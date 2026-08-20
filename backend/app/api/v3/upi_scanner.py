"""
UPI QR Code Scanner + Fraud Verification
Scan any QR code and verify payee before payment
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/v2/qr", tags=["upi-qr-scanner"])


class QRScanRequest(BaseModel):
    upi_id: Optional[str] = None
    upi_url: Optional[str] = None
    amount: Optional[float] = None
    merchant_name: Optional[str] = None


class PaymentVerifyRequest(BaseModel):
    payer_upi: str
    payee_upi: str
    amount: float
    merchant_name: Optional[str] = None


# Known suspicious UPI patterns
SUSPICIOUS_UPI_PATTERNS = [
    {"pattern": "test", "risk": 70, "reason": "Test UPI ID"},
    {"pattern": "demo", "risk": 60, "reason": "Demo UPI ID"},
    {"pattern": "personal", "risk": 40, "reason": "Personal account (not merchant)"},
    {"pattern": "new", "risk": 35, "reason": "Recently created account"},
]

# Known merchant fraud patterns
MERCHANT_FRAUD_PATTERNS = [
    {"pattern": "cashback", "risk": 85, "reason": "Cashback scam - promises fake cashback"},
    {"pattern": "reward", "risk": 75, "reason": "Reward scam - fake prize claims"},
    {"pattern": "refund", "risk": 80, "reason": "Refund scam - fake refund requests"},
    {"pattern": "verify", "risk": 70, "reason": "Verification scam - fake KYC update"},
    {"pattern": "urgent", "risk": 65, "reason": "Urgency tactic"},
]

# Known scam UPI IDs (community-reported)
SCAM_UPI_IDS = [
    "scammer@upi", "fraud123@paytm", "fakebank@google",
    "lotterywinner@ybl", "prizeclaim@okicici",
]


@router.post("/scan")
async def scan_upi_qr(req: QRScanRequest):
    """Scan and verify UPI QR code before payment"""
    upi_id = req.upi_id

    # Parse UPI URL if provided
    if req.upi_url and not upi_id:
        upi_id = extract_upi_from_url(req.upi_url)

    if not upi_id:
        return {"error": "No UPI ID found in scan"}

    return await verify_upi_id(upi_id, req.amount, req.merchant_name)


@router.post("/verify")
async def verify_payment(req: PaymentVerifyRequest):
    """Pre-payment verification"""
    return await verify_upi_id(
        req.payee_upi, req.amount, req.merchant_name, req.payer_upi
    )


@router.post("/check-upi")
async def check_upi_id(data: dict):
    """Quick UPI ID check"""
    upi_id = data.get("upi_id", "")
    return await verify_upi_id(upi_id)


async def verify_upi_id(upi_id: str, amount: float = None, merchant: str = None, payer: str = None) -> dict:
    """Full UPI verification with risk scoring"""
    upi_lower = upi_id.lower().strip()
    risk_factors = []
    total_risk = 0

    # 1. Check against known scam UPI IDs
    if upi_lower in SCAM_UPI_IDS:
        risk_factors.append({
            "factor": "known_scam_upi",
            "score": 99,
            "detail": "This UPI ID is in our scam database",
            "severity": "critical",
        })
        total_risk = 99

    # 2. Check suspicious patterns
    for pattern in SUSPICIOUS_UPI_PATTERNS:
        if pattern["pattern"] in upi_lower:
            risk_factors.append({
                "factor": "suspicious_pattern",
                "score": pattern["risk"],
                "detail": pattern["reason"],
                "severity": "high" if pattern["risk"] > 60 else "medium",
            })
            total_risk = max(total_risk, pattern["risk"])

    # 3. Check merchant name
    if merchant:
        for pattern in MERCHANT_FRAUD_PATTERNS:
            if pattern["pattern"] in merchant.lower():
                risk_factors.append({
                    "factor": "merchant_pattern",
                    "score": pattern["risk"],
                    "detail": f"Merchant name: {pattern['reason']}",
                    "severity": "high",
                })
                total_risk = max(total_risk, pattern["risk"])

    # 4. Amount analysis
    if amount:
        if amount > 200000:
            risk_factors.append({
                "factor": "high_amount",
                "score": 60,
                "detail": f"Very high amount: Rs.{amount:,.0f}",
                "severity": "high",
            })
            total_risk = max(total_risk, 60)
        elif amount > 50000:
            risk_factors.append({
                "factor": "medium_amount",
                "score": 30,
                "detail": f"High amount: Rs.{amount:,.0f}",
                "severity": "medium",
            })
            total_risk = max(total_risk, 30)

    # 5. UPI handle analysis
    handle = upi_lower.split("@")[-1] if "@" in upi_lower else ""
    trusted_handles = ["paytm", "okaxis", "okicici", "okhdfcbank", "oksbi", "ybl", "ibl", "axl", "apl"]
    if handle in trusted_handles:
        risk_factors.append({
            "factor": "trusted_platform",
            "score": -20,
            "detail": f"Verified platform: @{handle}",
            "severity": "positive",
        })
        total_risk = max(0, total_risk - 20)
    elif handle not in trusted_handles:
        risk_factors.append({
            "factor": "unknown_platform",
            "score": 15,
            "detail": f"Unknown UPI platform: @{handle}",
            "severity": "low",
        })
        total_risk = min(100, total_risk + 15)

    # 6. Payer-Payee same check
    if payer and payer.lower() == upi_lower:
        risk_factors.append({
            "factor": "self_transfer",
            "score": 50,
            "detail": "Sending to same UPI ID",
            "severity": "medium",
        })
        total_risk = max(total_risk, 50)

    total_risk = min(100, max(0, total_risk))

    # Recommendation
    if total_risk >= 80:
        recommendation = "BLOCK - Do NOT proceed with this payment"
        action = "block"
    elif total_risk >= 60:
        recommendation = "HIGH RISK - Verify payee identity before paying"
        action = "warn"
    elif total_risk >= 40:
        recommendation = "CAUTION - Double-check payee details"
        action = "caution"
    elif total_risk >= 20:
        recommendation = "LOW RISK - Appears safe but stay cautious"
        action = "allow_with_caution"
    else:
        recommendation = "SAFE - This appears to be a legitimate payee"
        action = "allow"

    return {
        "upi_id": upi_id,
        "handle": f"@{handle}" if handle else "unknown",
        "is_trusted_platform": handle in trusted_handles,
        "risk_score": total_risk,
        "recommendation": recommendation,
        "action": action,
        "risk_factors": risk_factors,
        "verified_at": datetime.now().isoformat(),
    }


def extract_upi_from_url(url: str) -> Optional[str]:
    """Extract UPI ID from UPI payment URL"""
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(parsed.query)
    if "pa" in params:
        return params["pa"][0]
    if "pn" in params:
        return params["pn"][0]
    # Try direct UPI ID format
    if "@" in url:
        return url.split("pa=")[-1].split("&")[0] if "pa=" in url else url
    return None
