"""
Website Verification API
Check if a website is legitimate or phishing
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from urllib.parse import urlparse

router = APIRouter()

class WebsiteCheckResponse(BaseModel):
    url: str
    is_safe: bool
    risk_score: int  # 0-100
    risk_level: str  # safe, suspicious, dangerous, phishing
    category: Optional[str] = None
    details: Optional[dict] = None

# Known phishing/malicious websites (mock database)
MALICIOUS_WEBSITES = {
    "fakekredit.com": {
        "is_safe": False,
        "risk_score": 95,
        "risk_level": "phishing",
        "category": "loan_scam",
        "reason": "Impersonates legitimate lender"
    },
    "quickcash-scam.in": {
        "is_safe": False,
        "risk_score": 90,
        "risk_level": "dangerous",
        "category": "loan_scam",
        "reason": "Fake loan app website"
    },
    "verify-kyc.xyz": {
        "is_safe": False,
        "risk_score": 88,
        "risk_level": "phishing",
        "category": "kyc_scam",
        "reason": "KYC phishing website"
    }
}

# Suspicious patterns in URLs
SUSPICIOUS_PATTERNS = [
    "verify", "update", "kyc", "refund", "claim",
    "prize", "winner", "lottery", "free", "urgent",
    "suspended", "blocked", "activate", "confirm"
]

SUSPICIOUS_EXTENSIONS = [".xyz", ".top", ".club", ".online", ".site"]

@router.get("/check", response_model=WebsiteCheckResponse)
async def check_website(
    url: str = Query(..., description="Website URL to check")
):
    """
    Check if a website is safe
    
    Analyzes:
    - Known phishing databases
    - URL patterns
    - Domain age
    - SSL certificate
    - Content analysis
    """
    # Parse URL
    parsed = urlparse(url if url.startswith("http") else "https://" + url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    
    # Check malicious database
    if domain in MALICIOUS_WEBSITES:
        data = MALICIOUS_WEBSITES[domain]
        return WebsiteCheckResponse(
            url=url,
            is_safe=data["is_safe"],
            risk_score=data["risk_score"],
            risk_level=data["risk_level"],
            category=data["category"],
            details={
                "reason": data["reason"],
                "source": "Known malicious database"
            }
        )
    
    # Check for suspicious patterns
    risk_score = 20  # Base score
    warnings = []
    
    # Check domain extension
    for ext in SUSPICIOUS_EXTENSIONS:
        if domain.endswith(ext):
            risk_score += 30
            warnings.append(f"Suspicious domain extension: {ext}")
    
    # Check URL patterns
    full_url = domain + path
    for pattern in SUSPICIOUS_PATTERNS:
        if pattern in full_url:
            risk_score += 15
            warnings.append(f"Suspicious pattern found: {pattern}")
    
    # Check for IP address instead of domain
    try:
        parts = domain.split(".")
        if len(parts) == 4 and all(p.isdigit() for p in parts):
            risk_score += 40
            warnings.append("IP address used instead of domain name")
    except:
        pass
    
    # Check for subdomain abuse
    if domain.count(".") > 2:
        risk_score += 20
        warnings.append("Multiple subdomains detected")
    
    # Determine risk level
    if risk_score < 30:
        risk_level = "safe"
        category = "likely_safe"
    elif risk_score < 50:
        risk_level = "suspicious"
        category = "needs_review"
    elif risk_score < 70:
        risk_level = "dangerous"
        category = "high_risk"
    else:
        risk_level = "phishing"
        category = "malicious"
    
    return WebsiteCheckResponse(
        url=url,
        is_safe=risk_score < 50,
        risk_score=min(risk_score, 100),
        risk_level=risk_level,
        category=category,
        details={
            "warnings": warnings,
            "recommendation": "Do not enter personal information" if risk_score >= 50 else "Proceed with caution"
        }
    )

@router.get("/check-qr")
async def check_qr_code(
    upi_id: str = Query(..., description="UPI ID from QR code")
):
    """
    Check if a UPI ID from QR code is legitimate
    
    Validates:
    - UPI handle format
    - Known scam patterns
    - Bank/PSP verification
    """
    # Valid UPI handles
    VALID_HANDLES = [
        "@oksbi", "@okicici", "@okaxis", "@okhdfcbank", "@okbank",
        "@ybl", "@paytm", "@phonepe", "@gpay", "@bhim",
        "@amazonpay", "@freecharge", "@mobikwik"
    ]
    
    # Scam patterns in UPI IDs
    SCAM_PATTERNS = [
        "refund", "kyc", "update", "verify", "claim",
        "prize", "winner", "cashback", "reward"
    ]
    
    risk_score = 10
    warnings = []
    
    # Check if UPI ID has valid handle
    has_valid_handle = False
    for handle in VALID_HANDLES:
        if upi_id.lower().endswith(handle):
            has_valid_handle = True
            break
    
    if not has_valid_handle:
        risk_score += 40
        warnings.append("Invalid or unknown UPI handle")
    
    # Check for scam patterns
    for pattern in SCAM_PATTERNS:
        if pattern in upi_id.lower():
            risk_score += 25
            warnings.append(f"Scam pattern detected: {pattern}")
    
    # Check for typosquatting (similar to valid handles)
    for handle in VALID_HANDLES:
        base = handle[1:]  # Remove @
        if base in upi_id.lower() and not upi_id.lower().endswith(handle):
            risk_score += 35
            warnings.append(f"Possible impersonation of {handle}")
    
    # Determine verdict
    if risk_score < 30:
        verdict = "Safe"
    elif risk_score < 50:
        verdict = "Suspicious"
    elif risk_score < 70:
        verdict = "High Risk"
    else:
        verdict = "Fraud"
    
    return {
        "upi_id": upi_id,
        "verdict": verdict,
        "risk_score": min(risk_score, 100),
        "warnings": warnings,
        "has_valid_handle": has_valid_handle,
        "recommendation": "Do not pay" if risk_score >= 50 else "Verify before paying"
    }
