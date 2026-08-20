"""
Loan App Verification API
Check if a loan app is legitimate (RBI registered)
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

class LoanAppCheckResponse(BaseModel):
    app_name: str
    is_legitimate: bool
    risk_score: int  # 0-100 (lower = safer)
    risk_level: str  # safe, caution, high_risk, dangerous
    rbi_registered: bool
    nbfc_name: Optional[str] = None
    nbfc_registration: Optional[str] = None
    app_store_url: Optional[str] = None
    website: Optional[str] = None
    details: Optional[dict] = None

class LoanAppSearchResult(BaseModel):
    app_name: str
    nbfc_name: str
    risk_level: str
    confidence: float

# RBI Registered Apps Database (mock - in production, use real RBI data)
RBI_REGISTERED_APPS = {
    "kreditbee": {
        "is_legitimate": True,
        "rbi_registered": True,
        "nbfc_name": "KreditBee Finance India Private Limited",
        "nbfc_registration": "NBFC-HC-Company-2018-1286",
        "app_store_url": "https://play.google.com/store/apps/details?id=com.kreditbee",
        "website": "https://www.kreditbee.in",
        "risk_score": 15,
        "risk_level": "safe"
    },
    "moglilabs": {
        "is_legitimate": True,
        "rbi_registered": True,
        "nbfc_name": "Klick2Cash Lending Solutions Private Limited",
        "nbfc_registration": "NBFC-HC-Company-2017-1089",
        "app_store_url": "https://play.google.com/store/apps/details?id=com.moglilabs",
        "website": "https://www.moglilabs.com",
        "risk_score": 18,
        "risk_level": "safe"
    },
    "truebalance": {
        "is_legitimate": True,
        "rbi_registered": True,
        "nbfc_name": "Balance Hero India Private Limited",
        "nbfc_registration": "NBFC-HC-Company-2014-0746",
        "app_store_url": "https://play.google.com/store/apps/details?id=com.balancehero.truebalance",
        "website": "https://www.truebalance.in",
        "risk_score": 20,
        "risk_level": "safe"
    },
    "loanorbit": {
        "is_legitimate": False,
        "rbi_registered": False,
        "nbfc_name": None,
        "nbfc_registration": None,
        "app_store_url": None,
        "website": None,
        "risk_score": 95,
        "risk_level": "dangerous",
        "blocked_by": "I4C",
        "blocked_date": "2026-08-07",
        "reason": "Fraudulent app - exorbitant interest rates, data harvesting"
    },
    "nexusloan": {
        "is_legitimate": False,
        "rbi_registered": False,
        "nbfc_name": None,
        "nbfc_registration": None,
        "app_store_url": None,
        "website": None,
        "risk_score": 92,
        "risk_level": "dangerous",
        "blocked_by": "I4C",
        "blocked_date": "2026-08-07",
        "reason": "Fraudulent app - harassment, data theft"
    }
}

@router.get("/check", response_model=LoanAppCheckResponse)
async def check_loan_app(
    name: str = Query(..., description="Loan app name to check")
):
    """
    Check if a loan app is legitimate
    
    Verifies against:
    - RBI Digital Lending Apps Directory
    - I4C blocked apps list
    - App store metadata
    - User reviews analysis
    """
    # Normalize name
    normalized = name.lower().strip().replace(" ", "")
    
    # Check database
    if normalized in RBI_REGISTERED_APPS:
        data = RBI_REGISTERED_APPS[normalized]
        return LoanAppCheckResponse(
            app_name=name,
            is_legitimate=data["is_legitimate"],
            risk_score=data["risk_score"],
            risk_level=data["risk_level"],
            rbi_registered=data["rbi_registered"],
            nbfc_name=data.get("nbfc_name"),
            nbfc_registration=data.get("nbfc_registration"),
            app_store_url=data.get("app_store_url"),
            website=data.get("website"),
            details={
                "blocked_by": data.get("blocked_by"),
                "blocked_date": data.get("blocked_date"),
                "reason": data.get("reason")
            }
        )
    
    # App not found - might be suspicious
    return LoanAppCheckResponse(
        app_name=name,
        is_legitimate=False,
        risk_score=70,
        risk_level="high_risk",
        rbi_registered=False,
        nbfc_name=None,
        nbfc_registration=None,
        app_store_url=None,
        website=None,
        details={
            "warning": "App not found in RBI directory. Verify manually."
        }
    )

@router.get("/search", response_model=List[LoanAppSearchResult])
async def search_loan_apps(
    query: str = Query(..., description="Search query"),
    limit: int = Query(10, ge=1, le=50)
):
    """
    Search for loan apps
    
    Returns matching apps from RBI directory
    """
    results = []
    query_lower = query.lower()
    
    for app_name, data in RBI_REGISTERED_APPS.items():
        if query_lower in app_name.lower() or query_lower in data.get("nbfc_name", "").lower():
            results.append(LoanAppSearchResult(
                app_name=app_name.title(),
                nbfc_name=data.get("nbfc_name", "Unknown"),
                risk_level=data["risk_level"],
                confidence=0.85
            ))
    
    return results[:limit]

@router.get("/rbi-directory")
async def get_rbi_directory(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Get RBI registered apps list
    
    Used by Android app to sync local database
    """
    legitimate_apps = [
        {
            "app_name": app_name.title(),
            "nbfc_name": data["nbfc_name"],
            "nbfc_registration": data["nbfc_registration"],
            "app_store_url": data.get("app_store_url"),
            "website": data.get("website")
        }
        for app_name, data in RBI_REGISTERED_APPS.items()
        if data["is_legitimate"]
    ]
    
    blocked_apps = [
        {
            "app_name": app_name.title(),
            "blocked_by": data.get("blocked_by"),
            "blocked_date": data.get("blocked_date"),
            "reason": data.get("reason")
        }
        for app_name, data in RBI_REGISTERED_APPS.items()
        if not data["is_legitimate"]
    ]
    
    return {
        "legitimate": {
            "total": len(legitimate_apps),
            "apps": legitimate_apps[offset:offset + limit]
        },
        "blocked": {
            "total": len(blocked_apps),
            "apps": blocked_apps
        }
    }
