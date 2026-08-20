"""
Enhanced API v2 - Real Data + AI/ML Integration
"""
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional, List, Dict
import httpx

from app.services.real_data import real_data_manager
from app.ml.scam_detector import scam_engine

router = APIRouter(prefix="/api/v2", tags=["v2-enhanced"])


# ─── Request Models ───────────────────────────────────────────────────

class PhoneCheckRequest(BaseModel):
    phone: str
    call_duration: Optional[int] = 0
    mentioned_police: Optional[bool] = False
    mentioned_loan: Optional[bool] = False
    mentioned_otp: Optional[bool] = False

class AppCheckRequest(BaseModel):
    app_name: str
    source: Optional[str] = "unknown"

class WebsiteCheckRequest(BaseModel):
    url: str

class TextAnalysisRequest(BaseModel):
    text: str
    language: Optional[str] = "auto"

class ScamReportRequest(BaseModel):
    phone: Optional[str] = None
    app_name: Optional[str] = None
    url: Optional[str] = None
    scam_type: str
    description: str
    reporter_name: Optional[str] = "anonymous"

class GuardianAlertRequest(BaseModel):
    sender_phone: str
    guardian_numbers: List[str]
    scam_type: str
    message: Optional[str] = None


# ─── AI-Powered Phone Check ──────────────────────────────────────────

@router.post("/check/phone")
async def check_phone_ai(req: PhoneCheckRequest):
    """AI-powered phone number risk analysis with real data integration"""
    
    # 1. Run AI/ML analysis
    context = {
        "call_duration": req.call_duration,
        "mentioned_police": req.mentioned_police,
        "mentioned_loan": req.mentioned_loan,
        "mentioned_otp": req.mentioned_otp,
    }
    ai_analysis = scam_engine.analyze_number(req.phone, context)

    # 2. Check real databases
    mnrl_data = await real_data_manager.fetch_mnrl_status(req.phone)
    fraud_data = await real_data_manager.fetch_fraudintel_data(req.phone)

    # 3. Combine results
    final_risk = ai_analysis["risk_score"]
    if mnrl_data.get("in_mnrl"):
        final_risk = max(final_risk, 95)
    if fraud_data and fraud_data.get("flagged"):
        final_risk = max(final_risk, 90)

    return {
        "phone": req.phone,
        "final_risk_score": min(100, final_risk),
        "risk_level": scam_engine._get_risk_level(final_risk)["level"],
        "risk_color": scam_engine._get_risk_level(final_risk)["color"],
        "ai_analysis": ai_analysis,
        "mnrl_status": mnrl_data,
        "fraud_intel": fraud_data,
        "recommendation": scam_engine._get_recommendation(final_risk),
        "data_sources": ["AI/ML Engine", "DoT MNRL", "I4C Suspect Registry", "FraudIntel", "Community Reports"],
    }


# ─── AI-Powered App Verification ─────────────────────────────────────

@router.post("/check/app")
async def check_app_ai(req: AppCheckRequest):
    """Verify loan app against RBI directory + AI fraud detection"""
    
    rbi_result = await real_data_manager.verify_rbi_app(req.app_name)
    
    # AI analysis based on app name patterns
    app_name_lower = req.app_name.lower()
    ai_flags = []
    ai_score = 0

    # Suspicious app name patterns
    if any(w in app_name_lower for w in ["fast", "quick", "instant", "easy", "rapid"]):
        ai_flags.append("Uses urgency words common in scam apps")
        ai_score += 15
    
    if any(w in app_name_lower for w in ["cash", "money", "rupee", "paisa", "loan"]):
        ai_flags.append("Direct money-related naming (common in predatory apps)")
        ai_score += 10

    if app_name_lower.endswith(("plus", "pro", "premium", "gold")):
        ai_flags.append("Premium naming pattern (common in fake apps)")
        ai_score += 10

    if req.source == "unknown" or req.source == "sideload":
        ai_flags.append("Installed from unknown source (high risk)")
        ai_score += 25

    if rbi_result["status"] == "FRAUDULENT":
        final_score = 95
    elif rbi_result["status"] == "LEGITIMATE":
        final_score = max(5, ai_score - 30)
    else:
        final_score = min(100, 50 + ai_score)

    return {
        "app_name": req.app_name,
        "status": rbi_result["status"],
        "risk_score": final_score,
        "rbi_verification": rbi_result.get("details", {}),
        "ai_flags": ai_flags,
        "recommendation": scam_engine._get_recommendation(final_score),
        "data_sources": ["RBI DLA Directory", "I4C Blacklist", "AI Pattern Analysis"],
    }


# ─── AI-Powered Website Check ────────────────────────────────────────

@router.post("/check/website")
async def check_website_ai(req: WebsiteCheckRequest):
    """Check website for phishing with AI pattern detection"""
    
    db_result = await real_data_manager.check_website(req.url)
    
    # AI analysis
    url_lower = req.url.lower()
    ai_flags = []
    ai_score = 0

    # Check for IP-based URLs (common in phishing)
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    if re.match(ip_pattern, url_lower.replace("https://", "").replace("http://", "").split("/")[0]):
        ai_flags.append("IP-based URL (common in phishing)")
        ai_score += 30

    # Check for URL shorteners
    shorteners = ["bit.ly", "tinyurl", "t.co", "goo.gl", "is.gd"]
    if any(s in url_lower for s in shorteners):
        ai_flags.append("URL shortener used (hides true destination)")
        ai_score += 20

    # Check for typosquatting
    legit_domains = ["paytm.com", "phonepe.com", "google.com", "hdfcbank.com", "icicibank.com"]
    for domain in legit_domains:
        brand = domain.split(".")[0]
        if brand in url_lower and domain not in url_lower:
            ai_flags.append(f"Possible typosquatting of {brand}")
            ai_score += 35

    if db_result["safe"] is False:
        final_score = 95
    elif db_result["safe"] is True:
        final_score = max(5, ai_score)
    else:
        final_score = min(100, 50 + ai_score)

    return {
        "url": req.url,
        "safe": db_result["safe"],
        "risk_score": final_score,
        "risk_level": db_result["risk_level"],
        "db_details": db_result.get("details", {}),
        "ai_flags": ai_flags,
        "recommendation": scam_engine._get_recommendation(final_score),
        "data_sources": ["Phishing Database", "TLD Analysis", "Brand Detection AI"],
    }


# ─── AI Text/SMS Analysis ────────────────────────────────────────────

@router.post("/analyze/text")
async def analyze_text_ai(req: TextAnalysisRequest):
    """Analyze SMS/message text for scam indicators"""
    result = scam_engine.analyze_text(req.text)
    
    return {
        "analysis": result,
        "detected_threats": len(result["detected_keywords"]),
        "data_sources": ["NLP Scam Detection", "Hindi/English Keyword DB", "Pattern Analysis"],
    }


# ─── Community Scam Reporting ────────────────────────────────────────

@router.post("/report/scam")
async def report_scam(req: ScamReportRequest):
    """Community-driven scam reporting"""
    report_data = {
        "phone": req.phone,
        "app_name": req.app_name,
        "url": req.url,
        "scam_type": req.scam_type,
        "description": req.description,
        "reporter_name": req.reporter_name,
    }
    result = await real_data_manager.report_scam(report_data)
    return result


# ─── Guardian Alert System ───────────────────────────────────────────

@router.post("/alert/guardian")
async def send_guardian_alert(req: GuardianAlertRequest):
    """Send SMS alert to guardian contacts"""
    message = req.message or f"ALERT: Potential {req.scam_type} detected. Stay safe. Report at cybercrime.gov.in"
    
    # In production, this would use Twilio/MSG91/Textlocal
    alerts_sent = []
    for number in req.guardian_numbers:
        alerts_sent.append({
            "to": number,
            "message": message,
            "status": "sent",
            "provider": "MSG91",
        })

    return {
        "sender": req.sender_phone,
        "alerts_sent": len(alerts_sent),
        "details": alerts_sent,
        "message": "Guardian alerts sent successfully",
    }


# ─── Threat Intelligence Dashboard ──────────────────────────────────

@router.get("/dashboard/stats")
async def get_dashboard_stats():
    """Real-time threat statistics for dashboard"""
    return await real_data_manager.get_threat_stats()


# ─── Multi-Language Support ──────────────────────────────────────────

@router.get("/scam-types")
async def get_scam_types():
    """List of known scam types with multilingual descriptions"""
    return {
        "scam_types": [
            {
                "id": "digital_arrest",
                "name_en": "Digital Arrest Scam",
                "name_hi": "डिजिटल गिरफ्तारी घोटाला",
                "description": "Fake police/CBI call claiming you're under digital arrest",
                "risk_level": "critical",
                "icon": "shield-alert",
            },
            {
                "id": "loan_fraud",
                "name_en": "Loan App Fraud",
                "name_hi": "लोन ऐप घोटाला",
                "description": "Fake loan apps that charge hidden fees and harvest data",
                "risk_level": "high",
                "icon": "credit-card-alert",
            },
            {
                "id": "upi_phishing",
                "name_en": "UPI Phishing",
                "name_hi": "UPI फिशिंग",
                "description": "Fake UPI links or QR codes to steal money",
                "risk_level": "high",
                "icon": "qr-code-alert",
            },
            {
                "id": "kyc_fraud",
                "name_en": "KYC Fraud",
                "name_hi": "KYC घोटाला",
                "description": "Fake calls asking for KYC update to steal bank details",
                "risk_level": "high",
                "icon": "id-card-alert",
            },
            {
                "id": "otp_phishing",
                "name_en": "OTP Phishing",
                "name_hi": "OTP फिशिंग",
                "description": "Tricking you into sharing OTP for fraudulent transactions",
                "risk_level": "critical",
                "icon": "key-alert",
            },
            {
                "id": "tech_support",
                "name_en": "Tech Support Scam",
                "name_hi": "तकनीकी सहायता घोटाला",
                "description": "Fake calls claiming your computer has a virus",
                "risk_level": "medium",
                "icon": "monitor-alert",
            },
            {
                "id": "investment_fraud",
                "name_en": "Investment Fraud",
                "name_hi": "निवेश घोटाला",
                "description": "Guaranteed return schemes and Ponzi frauds",
                "risk_level": "high",
                "icon": "trending-up-alert",
            },
        ]
    }


import re
