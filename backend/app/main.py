"""
SurakshaShield Backend API v3
AI-Powered Complete Fraud Protection for 424 Million UPI Users
Real Data + ML + Vernacular + Bank API + WhatsApp + Dashboard + UPI Scanner + Scam Map
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("SurakshaShield API v3 Starting...")
    print("Modules: AI/ML, Real Data, Vernacular, Bank API, WhatsApp Bot, Dashboard, UPI Scanner, Scam Map")
    yield
    print("SurakshaShield API Shutting Down...")

app = FastAPI(
    title="SurakshaShield API v3",
    description="AI-Powered Complete Fraud Protection for India | 10 Languages | Real-time Dashboard | Bank API",
    version="3.0.0",
    lifespan=lifespan,
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "app": "SurakshaShield",
        "version": "3.0.0",
        "modules": {
            "ai_ml_engine": "active",
            "tensorflow_lite_classifier": "active",
            "real_data_integration": "active",
            "vernacular_10_languages": "active",
            "whatsapp_bot": "active",
            "live_dashboard": "active",
            "upi_qr_scanner": "active",
            "india_scam_map": "active",
            "bank_api": "active",
            "call_transcript_ai": "active",
            "offline_mode": "ready",
        },
        "total_endpoints": 35,
    }

# V1 APIs
from app.api import numbers, apps, websites, alerts
app.include_router(numbers.router, prefix="/api/v1/numbers", tags=["V1 - Numbers"])
app.include_router(apps.router, prefix="/api/v1/apps", tags=["V1 - Apps"])
app.include_router(websites.router, prefix="/api/v1/websites", tags=["V1 - Websites"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["V1 - Alerts"])

# V2 APIs
from app.api.v2.enhanced_api import router as v2_router
app.include_router(v2_router, tags=["V2 - AI-Powered"])

# V3 APIs
from app.api.v3.whatsapp_bot import router as wa_router
from app.api.v3.live_dashboard import router as dash_router
from app.api.v3.upi_scanner import router as upi_router
from app.api.v3.call_analysis import router as call_router
app.include_router(wa_router, tags=["V3 - WhatsApp Bot"])
app.include_router(dash_router, tags=["V3 - Live Dashboard"])
app.include_router(upi_router, tags=["V3 - UPI Scanner"])
app.include_router(call_router, tags=["V3 - Call Transcript AI"])

# Bank API
from app.api.bank_api import router as bank_router
app.include_router(bank_router, tags=["Bank Partnership"])

# Vernacular & Offline
from app.services.vernacular import vernacular_engine, offline_engine

@app.get("/api/v2/languages", tags=["Vernacular"])
async def get_supported_languages():
    return {"languages": vernacular_engine.get_all_languages()}

@app.post("/api/v2/offline/check", tags=["Offline"])
async def offline_check(data: dict):
    return offline_engine.get_offline_risk_score(data.get("phone", ""))

@app.get("/", tags=["Root"])
async def root():
    return {
        "app": "SurakshaShield",
        "version": "3.0.0",
        "tagline": "Complete Fraud Protection for 424 Million UPI Users",
        "docs": "/docs",
        "apis": {
            "v1": "/api/v1/{numbers,apps,websites,alerts}",
            "v2_ai": "/api/v2/{check/phone, check/app, check/website, analyze/text}",
            "v3_whatsapp": "/api/whatsapp/check",
            "v3_dashboard": "/api/v2/dashboard/live",
            "v3_scam_map": "/api/v2/dashboard/india-map",
            "v3_upi_scanner": "/api/v2/qr/scan",
            "v3_call_ai": "/api/v2/call-analysis/analyze",
            "v3_threat_intel": "/api/v2/dashboard/threat-intel",
            "bank": "/api/bank/{dashboard, transaction/risk-score, compliance}",
        },
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
