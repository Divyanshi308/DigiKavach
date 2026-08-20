"""
Call Transcript AI Analysis
Analyze forwarded call recordings/transcripts for scam detection
Hindi + English + Regional language support
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/v2/call-analysis", tags=["call-transcript-ai"])


class TranscriptRequest(BaseModel):
    transcript: str
    language: Optional[str] = "auto"
    caller_number: Optional[str] = None
    call_duration_seconds: Optional[int] = None


class AudioFeatureRequest(BaseModel):
    transcript: str
    duration_seconds: int
    pause_count: int = 0
    words_per_minute: int = 150
    silence_ratio: float = 0.2
    background_noise_db: float = 30
    caller_id_suspicious: bool = False
    recent_call_count: int = 0
    call_hour: int = 12


@router.post("/analyze")
async def analyze_transcript(req: TranscriptRequest):
    """Analyze a call transcript for scam indicators"""
    from app.ml.classifier import scam_classifier

    result = scam_classifier.analyze_transcript(req.transcript, req.language)

    # Extract caller risk from number if provided
    caller_risk = None
    if req.caller_number:
        from app.services.real_data import real_data_manager
        mnrl = await real_data_manager.fetch_mnrl_status(req.caller_number)
        caller_risk = {
            "number": req.caller_number[:6] + "***",
            "in_mnrl": mnrl.get("in_mnrl", False),
            "risk_level": mnrl.get("risk_level", "unknown"),
        }

    return {
        "analysis": result,
        "caller_info": caller_risk,
        "call_metadata": {
            "duration_seconds": req.call_duration_seconds,
            "timestamp": datetime.now().isoformat(),
        },
        "recommendation": _get_recommendation(result["overall_risk"]),
        "action_items": _get_action_items(result),
    }


@router.post("/analyze-audio-features")
async def analyze_audio_features(req: AudioFeatureRequest):
    """Analyze extracted audio features for scam classification"""
    from app.ml.classifier import scam_classifier

    audio_features = {
        "transcript": req.transcript,
        "pause_count": req.pause_count,
        "words_per_minute": req.words_per_minute,
        "silence_ratio": req.silence_ratio,
        "background_noise_db": req.background_noise_db,
    }

    metadata = {
        "duration_seconds": req.duration_seconds,
        "hour": req.call_hour,
        "recent_call_count": req.recent_call_count,
        "caller_id_suspicious": req.caller_id_suspicious,
    }

    result = scam_classifier.classify_call(audio_features, metadata)

    return {
        "classification": result,
        "audio_quality": {
            "duration_seconds": req.duration_seconds,
            "words_per_minute": req.words_per_minute,
            "silence_ratio": f"{req.silence_ratio * 100:.0f}%",
        },
    }


@router.post("/batch-analyze")
async def batch_analyze(transcripts: list):
    """Analyze multiple transcripts at once (for bulk checking)"""
    from app.ml.classifier import scam_classifier

    results = []
    for item in transcripts[:10]:  # Max 10 at once
        result = scam_classifier.analyze_transcript(
            item.get("transcript", ""),
            item.get("language", "auto")
        )
        results.append({
            "id": item.get("id", "unknown"),
            "risk_score": result["overall_risk"],
            "scam_types": result["scam_types_detected"],
            "language": result["language"],
        })

    return {
        "results": results,
        "analyzed_count": len(results),
        "high_risk_count": sum(1 for r in results if r["risk_score"] >= 60),
    }


def _get_recommendation(risk_score: int) -> str:
    if risk_score >= 80:
        return "CRITICAL: This is almost certainly a scam call. Report to 1930 immediately. Block the number."
    elif risk_score >= 60:
        return "HIGH RISK: Strong scam indicators detected. Do NOT share any personal/financial information."
    elif risk_score >= 40:
        return "MODERATE RISK: Some suspicious patterns found. Verify caller identity through official channels."
    elif risk_score >= 20:
        return "LOW RISK: Minor indicators found. Stay cautious but likely legitimate."
    else:
        return "SAFE: No significant scam indicators detected."


def _get_action_items(result: dict) -> list:
    items = []
    for indicator in result.get("critical_indicators", []):
        if "OTP" in indicator:
            items.append("NEVER share OTP with anyone over phone")
        if "Remote" in indicator:
            items.append("NEVER install remote access apps (AnyDesk/TeamViewer) on caller's instruction")
        if "Authority" in indicator:
            items.append("Verify by calling the agency directly (CBI: 011-24368630)")
    if result["overall_risk"] >= 60:
        items.append("Report this number at cybercrime.gov.in")
        items.append("Block this number on your phone")
        items.append("Alert your family members about this scam")
    return items
