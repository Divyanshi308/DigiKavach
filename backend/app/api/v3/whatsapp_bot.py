"""
WhatsApp Bot Integration
Forward scam messages/calls to check
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/whatsapp", tags=["whatsapp-bot"])


class WhatsAppMessage(BaseModel):
    phone_number: str
    message: str
    message_type: str = "text"  # text, image, audio
    timestamp: Optional[str] = None


class ScamForward(BaseModel):
    sender: str
    content: str
    forward_type: str  # message, call_recording, contact
    language: Optional[str] = "auto"


# Known scam message templates
SCAM_TEMPLATES = [
    {
        "id": "lottery",
        "pattern": "congratulations|you won|lottery|prize|claim your",
        "type": "Lottery Scam",
        "severity": "high",
        "sample_reply": "This is a LOTTERY SCAM. No real company randomly contacts people with prizes. Do NOT click any links or share personal info.",
    },
    {
        "id": "kyc",
        "pattern": "kyc.*(?:expir|update|verif)|account.*(?:block|suspend|freez)",
        "type": "KYC Fraud",
        "severity": "high",
        "sample_reply": "This is KYC FRAUD. Banks never ask for KYC updates via WhatsApp. Contact your bank directly using the number on your card.",
    },
    {
        "id": "job",
        "pattern": "work from home|earn.*(?:daily|weekly|monthly)| guaranteed income|investment",
        "type": "Job/Investment Scam",
        "severity": "high",
        "sample_reply": "This is a JOB/INVESTMENT SCAM. No legitimate company promises guaranteed daily income. Do NOT pay any registration fee.",
    },
    {
        "id": "loan",
        "pattern": "instant loan|loan approved|quick cash|no document.*loan",
        "type": "Loan Scam",
        "severity": "high",
        "sample_reply": "This is a LOAN SCAM. Real loans require documentation. Do NOT share Aadhaar/PAN details or pay upfront fees.",
    },
    {
        "id": "phishing",
        "pattern": "click here|verify.*account|update.*details|confirm.*payment|won.*prize",
        "type": "Phishing Link",
        "severity": "critical",
        "sample_reply": "This is a PHISHING message. Do NOT click any links. The URL likely leads to a fake website that steals your data.",
    },
    {
        "id": "family_emergency",
        "pattern": "mom.*(?:hospit|accident|urg)|dad.*(?:hospit|accident|urg)|family.*emergency.*money",
        "type": "Family Emergency Scam",
        "severity": "critical",
        "sample_reply": "This is likely a FAMILY EMERGENCY SCAM. Call your family member directly before sending any money. Scammers impersonate relatives in distress.",
    },
    {
        "id": "tax_refund",
        "pattern": "tax refund|income tax.*(?:notice|refund|due)|gst.*refund",
        "type": "Tax Scam",
        "severity": "high",
        "sample_reply": "This is a TAX SCAM. The Income Tax Department never contacts via WhatsApp. Log into the official portal to check your status.",
    },
    {
        "id": "upi_collect",
        "pattern": "upi.*(?:collect|request|pay)|google pay|phonepe|paytm.*(?:request|collect)",
        "type": "UPI Fraud Attempt",
        "severity": "critical",
        "sample_reply": "This is a UPI FRAUD attempt. NEVER approve a UPI collect request from unknown numbers. Your money will be instantly deducted.",
    },
]

WHATSAPP_RESPONSE_TEMPLATES = {
    "scam_detected": "🚨 SCAM DETECTED!\n\nType: {scam_type}\nSeverity: {severity}\n\n{reply}\n\nTo report: Forward to 1930 (Cyber Crime)\nTo check any number/app/website: Visit SurakshaShield",
    "safe": "✅ No scam detected in this message.\n\nHowever, always verify before sharing personal information.\n\nTo check: Send any phone number, app name, or URL to this bot.",
    "unknown": "❓ Could not analyze this message.\n\nYou can manually check:\n- Phone number: Send just the number\n- App name: Send 'check app [name]'\n- Website: Send 'check website [url]'",
}


@router.post("/webhook")
async def whatsapp_webhook(msg: WhatsAppMessage):
    """WhatsApp Business API webhook"""
    result = await analyze_whatsapp_message(msg.message)
    return {
        "status": "ok",
        "reply": result["response"],
        "analysis": result["analysis"],
    }


@router.post("/check")
async def check_forwarded_message(req: ScamForward):
    """Check a forwarded scam message/call"""
    from app.ml.classifier import scam_classifier

    # Run AI analysis
    analysis = scam_classifier.analyze_transcript(req.content, req.language)

    # Find matching scam template
    import re
    matched_template = None
    for template in SCAM_TEMPLATES:
        if re.search(template["pattern"], req.content.lower()):
            matched_template = template
            break

    if matched_template or analysis["overall_risk"] > 60:
        scam_type = matched_template["type"] if matched_template else "Unknown Scam"
        severity = matched_template["severity"] if matched_template else "high"
        reply = matched_template["sample_reply"] if matched_template else "This message shows scam indicators. Be cautious."

        response = WHATSAPP_RESPONSE_TEMPLATES["scam_detected"].format(
            scam_type=scam_type,
            severity=severity.upper(),
            reply=reply,
        )
    elif analysis["overall_risk"] < 30:
        response = WHATSAPP_RESPONSE_TEMPLATES["safe"]
    else:
        response = WHATSAPP_RESPONSE_TEMPLATES["unknown"]

    return {
        "response": response,
        "analysis": {
            "risk_score": analysis["overall_risk"],
            "language": analysis["language"],
            "scam_types": analysis["scam_types_detected"],
            "critical_indicators": analysis["critical_indicators"],
            "findings": analysis["findings"],
        },
    }


@router.get("/scam-templates")
async def get_scam_templates():
    """List of known scam message templates for user education"""
    return {
        "templates": [
            {
                "type": t["type"],
                "severity": t["severity"],
                "example_keywords": t["pattern"],
                "advice": t["sample_reply"],
            }
            for t in SCAM_TEMPLATES
        ]
    }


async def analyze_whatsapp_message(message: str) -> dict:
    from app.ml.classifier import scam_classifier
    import re

    analysis = scam_classifier.analyze_transcript(message)

    matched = None
    for template in SCAM_TEMPLATES:
        if re.search(template["pattern"], message.lower()):
            matched = template
            break

    if matched:
        response = WHATSAPP_RESPONSE_TEMPLATES["scam_detected"].format(
            scam_type=matched["type"],
            severity=matched["severity"].upper(),
            reply=matched["sample_reply"],
        )
    elif analysis["overall_risk"] < 30:
        response = WHATSAPP_RESPONSE_TEMPLATES["safe"]
    else:
        response = WHATSAPP_RESPONSE_TEMPLATES["unknown"]

    return {"response": response, "analysis": analysis}
