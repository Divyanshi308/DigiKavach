"""
Alerts API
Manage guardian alerts and notifications
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

class GuardianSetup(BaseModel):
    user_id: str
    guardian_name: str
    guardian_phone: str
    relationship: str  # parent, spouse, sibling, friend

class AlertResponse(BaseModel):
    alert_id: str
    user_id: str
    alert_type: str
    message: str
    timestamp: datetime
    status: str  # sent, delivered, failed

class AlertHistory(BaseModel):
    alerts: List[AlertResponse]
    total: int

# In-memory storage (use database in production)
GUARDIANS_DB = {}
ALERTS_DB = {}

@router.post("/setup-guardian")
async def setup_guardian(guardian: GuardianSetup):
    """
    Setup a guardian contact for emergency alerts
    
    Guardian receives SMS when:
    - User answers suspicious call
    - User opens banking app during unknown call
    - User tries to pay scammer
    """
    # Store guardian
    GUARDIANS_DB[guardian.user_id] = {
        "name": guardian.guardian_name,
        "phone": guardian.guardian_phone,
        "relationship": guardian.relationship,
        "created_at": datetime.now()
    }
    
    return {
        "status": "success",
        "message": f"Guardian {guardian.guardian_name} added successfully",
        "guardian": {
            "name": guardian.guardian_name,
            "relationship": guardian.relationship
        }
    }

@router.get("/guardian/{user_id}")
async def get_guardian(user_id: str):
    """Get guardian details for a user"""
    if user_id not in GUARDIANS_DB:
        raise HTTPException(status_code=404, detail="No guardian found")
    
    return GUARDIANS_DB[user_id]

@router.post("/send-alert")
async def send_alert(
    user_id: str,
    alert_type: str,
    message: str
):
    """
    Send alert to guardian
    
    Alert types:
    - suspicious_call: User answered a scam call
    - banking_during_call: User opened banking app during unknown call
    - payment_attempt: User tried to pay suspicious number
    - website_warning: User visited phishing website
    """
    # Check if guardian exists
    if user_id not in GUARDIANS_DB:
        raise HTTPException(status_code=404, detail="No guardian configured")
    
    guardian = GUARDIANS_DB[user_id]
    
    # Create alert
    alert_id = f"ALT{int(datetime.now().timestamp())}"
    alert = AlertResponse(
        alert_id=alert_id,
        user_id=user_id,
        alert_type=alert_type,
        message=message,
        timestamp=datetime.now(),
        status="sent"
    )
    
    # Store alert
    if user_id not in ALERTS_DB:
        ALERTS_DB[user_id] = []
    ALERTS_DB[user_id].append(alert)
    
    # In production: Send SMS via Twilio/MSG91
    # sms_service.send(guardian["phone"], message)
    
    return {
        "status": "success",
        "alert_id": alert_id,
        "guardian_notified": guardian["name"],
        "message": f"Alert sent to {guardian['name']} ({guardian['relationship']})"
    }

@router.get("/history/{user_id}", response_model=AlertHistory)
async def get_alert_history(
    user_id: str,
    limit: int = Query(50, ge=1, le=100)
):
    """Get alert history for a user"""
    alerts = ALERTS_DB.get(user_id, [])
    return AlertHistory(
        alerts=alerts[-limit:],
        total=len(alerts)
    )

@router.post("/emergency-sms")
async def send_emergency_sms(
    user_id: str,
    message: str = "EMERGENCY: I might be in trouble. Please call me immediately."
):
    """
    Send emergency SMS to guardian
    
    Triggered when:
    - User manually triggers emergency
    - App detects high-risk situation
    """
    if user_id not in GUARDIANS_DB:
        raise HTTPException(status_code=404, detail="No guardian configured")
    
    guardian = GUARDIANS_DB[user_id]
    
    # In production: Send SMS via Twilio/MSG91
    # sms_service.send(guardian["phone"], message)
    
    return {
        "status": "success",
        "message": f"Emergency SMS sent to {guardian['name']}",
        "guardian_phone": guardian["phone"]
    }
