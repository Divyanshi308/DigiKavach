"""
Phone Number Verification API
Check if a number is a known scam number
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class NumberCheckResponse(BaseModel):
    number: str
    is_scam: bool
    risk_score: int  # 0-100
    risk_level: str  # safe, suspicious, dangerous, scam
    source: str
    reports: int
    last_updated: datetime
    details: Optional[dict] = None

class NumberReportRequest(BaseModel):
    number: str
    report_type: str  # scam, spam, fraud, harassment
    description: Optional[str] = None

# Known scam numbers database (mock - in production, use real database)
SCAM_NUMBERS_DB = {
    "+919876543210": {
        "is_scam": True,
        "risk_score": 95,
        "risk_level": "scam",
        "source": "DoT MNRL",
        "reports": 1250,
        "type": "digital_arrest_scam",
        "active": True
    },
    "+911234567890": {
        "is_scam": True,
        "risk_score": 88,
        "risk_level": "dangerous",
        "source": "I4C Registry",
        "reports": 890,
        "type": "loan_fraud",
        "active": True
    },
    "+919999999999": {
        "is_scam": False,
        "risk_score": 15,
        "risk_level": "safe",
        "source": "Verified",
        "reports": 0,
        "type": None,
        "active": False
    }
}

@router.get("/check", response_model=NumberCheckResponse)
async def check_number(
    number: str = Query(..., description="Phone number to check (with country code)")
):
    """
    Check if a phone number is a known scam number
    
    Returns risk assessment based on:
    - DoT MNRL database
    - I4C Suspect Registry
    - RBI fraud reports
    - Community reports
    """
    # Normalize number
    normalized = number.strip().replace(" ", "").replace("-", "")
    if not normalized.startswith("+91"):
        if normalized.startswith("91") and len(normalized) == 12:
            normalized = "+" + normalized
        elif len(normalized) == 10:
            normalized = "+91" + normalized
    
    # Check database
    if normalized in SCAM_NUMBERS_DB:
        data = SCAM_NUMBERS_DB[normalized]
        return NumberCheckResponse(
            number=normalized,
            is_scam=data["is_scam"],
            risk_score=data["risk_score"],
            risk_level=data["risk_level"],
            source=data["source"],
            reports=data["reports"],
            last_updated=datetime.now(),
            details={
                "type": data["type"],
                "active": data["active"]
            }
        )
    
    # Number not in database - assume safe
    return NumberCheckResponse(
        number=normalized,
        is_scam=False,
        risk_score=10,
        risk_level="safe",
        source="Not in database",
        reports=0,
        last_updated=datetime.now(),
        details=None
    )

@router.post("/report")
async def report_number(report: NumberReportRequest):
    """
    Report a phone number as scam/spam
    
    This helps build community database
    """
    # In production, save to database
    return {
        "status": "success",
        "message": f"Number {report.number} reported as {report.report_type}",
        "report_id": "RPT" + str(datetime.now().timestamp())
    }

@router.get("/scam-list")
async def get_scam_list(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Get list of known scam numbers
    
    Used by Android app to sync local database
    """
    scam_numbers = [
        {
            "number": num,
            "risk_score": data["risk_score"],
            "type": data["type"],
            "reports": data["reports"]
        }
        for num, data in SCAM_NUMBERS_DB.items()
        if data["is_scam"]
    ]
    
    return {
        "total": len(scam_numbers),
        "limit": limit,
        "offset": offset,
        "numbers": scam_numbers[offset:offset + limit]
    }
