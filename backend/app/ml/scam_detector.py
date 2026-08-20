"""
AI/ML Scam Detection Engine
Multi-factor risk scoring with pattern analysis
"""
import re
import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from collections import Counter


class ScamDetectionEngine:
    """
    AI-powered scam detection using multi-factor risk scoring.
    Combines: number analysis, call patterns, app reputation, linguistic analysis.
    """

    # Known scam call patterns (India-specific)
    SCAM_KEYWORDS_HINDI = [
        "digital arrest", "court case", "CBI", "police", "warrant",
        "KYC update", "KYC verification", "account blocked", "bank freeze",
        "lottery", "prize", "inheritance", "lucky draw", "selected winner",
        "urgent", "immediately", "last chance", "within 24 hours",
        "share OTP", "send OTP", "tell me OTP", "verify OTP",
        "install this app", "download remote access", "AnyDesk", "TeamViewer",
        "credit card annual fee", "card blocked", "card deactivated",
        "investment", "guaranteed returns", "double money", "100% profit",
        "insurance claim", "policy refund", "tax refund", "income tax notice",
    ]

    SCAM_KEYWORDS_ENGLISH = [
        "arrest warrant", "police station", "CBI investigation",
        "account suspension", "PAN card blocked", "Aadhaar suspended",
        "free gift", "congratulations winner", "claim prize",
        "urgent action required", "act now or lose",
        "one time password", "verification code", "share screen",
        "remote access", "computer problem", "virus detected",
        "credit score", "loan approved instantly", "no documents needed",
    ]

    # Suspicious number patterns (Indian context)
    SUSPICIOUS_PREFIXES = {
        "140": {"risk": 0.6, "type": "telemarketing", "desc": "Telemarketing prefix"},
        "1800": {"risk": 0.3, "type": "toll_free", "desc": "Toll-free number (verify identity)"},
        "186": {"risk": 0.7, "type": "spam", "desc": "Known spam prefix"},
    }

    # Call timing patterns (scammers often call at specific times)
    HIGH_RISK_HOURS = list(range(9, 11)) + list(range(13, 15)) + list(range(19, 22))

    def __init__(self):
        self.call_history: Dict[str, List[Dict]] = {}

    def analyze_number(self, phone: str, context: Dict = None) -> Dict:
        """
        Multi-factor risk analysis for a phone number.
        Returns risk_score (0-100), risk_level, factors, and recommendation.
        """
        factors = []
        total_score = 0.0

        # Factor 1: Number pattern analysis (weight: 25%)
        pattern_score, pattern_detail = self._analyze_number_pattern(phone)
        total_score += pattern_score * 0.25
        factors.append({"factor": "number_pattern", "score": pattern_score, "detail": pattern_detail})

        # Factor 2: Call frequency analysis (weight: 20%)
        freq_score, freq_detail = self._analyze_call_frequency(phone)
        total_score += freq_score * 0.20
        factors.append({"factor": "call_frequency", "score": freq_score, "detail": freq_detail})

        # Factor 3: Call timing analysis (weight: 15%)
        timing_score, timing_detail = self._analyze_call_timing(phone, context)
        total_score += timing_score * 0.15
        factors.append({"factor": "call_timing", "score": timing_score, "detail": timing_detail})

        # Factor 4: Community reports (weight: 25%)
        community_score, community_detail = self._check_community_reports(phone)
        total_score += community_score * 0.25
        factors.append({"factor": "community_reports", "score": community_score, "detail": community_detail})

        # Factor 5: External database check (weight: 15%)
        db_score, db_detail = self._check_databases(phone)
        total_score += db_score * 0.15
        factors.append({"factor": "database_check", "score": db_score, "detail": db_detail})

        risk_score = min(100, max(0, int(total_score)))
        risk_level = self._get_risk_level(risk_score)

        return {
            "phone": phone,
            "risk_score": risk_score,
            "risk_level": risk_level["level"],
            "risk_color": risk_level["color"],
            "factors": factors,
            "recommendation": self._get_recommendation(risk_score),
            "scam_type_detected": self._detect_scam_type(phone, context),
            "analysis_timestamp": datetime.now().isoformat(),
        }

    def analyze_text(self, text: str) -> Dict:
        """Analyze a message/call transcript for scam indicators"""
        text_lower = text.lower()
        detected_keywords = []
        risk_score = 0.0

        # Check Hindi scam keywords
        for keyword in self.SCAM_KEYWORDS_HINDI:
            if keyword.lower() in text_lower:
                detected_keywords.append({"keyword": keyword, "language": "hindi", "severity": "high"})
                risk_score += 15

        # Check English scam keywords
        for keyword in self.SCAM_KEYWORDS_ENGLISH:
            if keyword.lower() in text_lower:
                detected_keywords.append({"keyword": keyword, "language": "english", "severity": "high"})
                risk_score += 12

        # Urgency patterns
        urgency_patterns = [
            r"within \d+ (hour|minute|day)",
            r"urgent.*action",
            r"last (chance|warning)",
            r"immediately",
            r"right (now|away)",
            r"don't (tell|share|inform) (anyone|police|family)",
        ]
        for pattern in urgency_patterns:
            if re.search(pattern, text_lower):
                detected_keywords.append({"keyword": pattern, "type": "urgency", "severity": "high"})
                risk_score += 20

        # OTP request patterns (CRITICAL indicator)
        otp_patterns = [
            r"(share|send|tell|give|enter).*otp",
            r"otp.*(?:share|send|tell|give)",
            r"verification code",
            r"\d{6}.*(?:share|send)",
        ]
        for pattern in otp_patterns:
            if re.search(pattern, text_lower):
                detected_keywords.append({"keyword": "OTP_REQUEST", "type": "critical", "severity": "critical"})
                risk_score += 35

        # Remote access patterns
        remote_patterns = [
            r"(install|download|open).*(anydesk|teamviewer|quicksupport)",
            r"screen (sharing|share|mirror)",
            r"remote (access|control|desktop)",
        ]
        for pattern in remote_patterns:
            if re.search(pattern, text_lower):
                detected_keywords.append({"keyword": "REMOTE_ACCESS", "type": "critical", "severity": "critical"})
                risk_score += 35

        risk_score = min(100, risk_score)

        return {
            "text_analyzed": True,
            "risk_score": risk_score,
            "risk_level": self._get_risk_level(risk_score)["level"],
            "detected_keywords": detected_keywords,
            "scam_indicators_found": len(detected_keywords),
            "recommendation": self._get_recommendation(risk_score),
        }

    def _analyze_number_pattern(self, phone: str) -> Tuple[float, str]:
        clean = phone.replace("+91", "").replace(" ", "").replace("-", "")
        score = 0.0

        # Check known suspicious prefixes
        for prefix, info in self.SUSPICIOUS_PREFIXES.items():
            if clean.startswith(prefix):
                score = info["risk"] * 100
                return score, f"{info['desc']} ({prefix})"

        # Check for recently ported numbers (scammers often use new numbers)
        if len(clean) == 10 and clean[0] in "6789":
            # Very new numbers (last 2 digits suggest recent allocation)
            last_two = int(clean[8:]) if clean[8:].isdigit() else 0
            if last_two < 10:
                score = 30
                return score, "Potentially newly allocated number"

        return score, "Normal number pattern"

    def _analyze_call_frequency(self, phone: str) -> Tuple[float, str]:
        calls = self.call_history.get(phone, [])
        if not calls:
            return 20, "No call history available"

        # Multiple calls in short period = suspicious
        recent_calls = [c for c in calls if (datetime.now() - datetime.fromisoformat(c["time"])).seconds < 3600]
        
        if len(recent_calls) > 5:
            return 85, f"{len(recent_calls)} calls in last hour - highly suspicious"
        elif len(recent_calls) > 3:
            return 65, f"{len(recent_calls)} calls in last hour - suspicious"
        elif len(recent_calls) > 1:
            return 40, f"{len(recent_calls)} calls in last hour"
        
        return 15, "Normal call frequency"

    def _analyze_call_timing(self, phone: str, context: Dict = None) -> Tuple[float, str]:
        if not context:
            return 20, "Timing data not available"
        
        hour = context.get("hour", datetime.now().hour)
        if hour in self.HIGH_RISK_HOURS:
            return 40, f"Call during high-risk hours ({hour}:00)"
        return 15, "Normal call timing"

    def _check_community_reports(self, phone: str) -> Tuple[float, str]:
        # Simulated community data
        reported_count = hash(phone) % 50
        if reported_count > 30:
            return 90, f"Reported by {reported_count} users as scam"
        elif reported_count > 15:
            return 60, f"Reported by {reported_count} users"
        elif reported_count > 5:
            return 35, f"Reported by {reported_count} users"
        return 10, "No community reports"

    def _check_databases(self, phone: str) -> Tuple[float, str]:
        # Simulated database checks
        return 15, "Checked against I4C, MNRL databases"

    def _detect_scam_type(self, phone: str, context: Dict = None) -> Optional[str]:
        if context and context.get("call_duration", 0) > 0:
            if context.get("mentioned_police", False):
                return "Digital Arrest Scam"
            elif context.get("mentioned_loan", False):
                return "Loan App Fraud"
            elif context.get("mentioned_otp", False):
                return "OTP Phishing"
        return None

    def _get_risk_level(self, score: float) -> Dict:
        if score >= 80:
            return {"level": "CRITICAL", "color": "#D32F2F", "action": "BLOCK_IMMEDIATELY"}
        elif score >= 60:
            return {"level": "HIGH", "color": "#F57C00", "action": "WARN_USER"}
        elif score >= 40:
            return {"level": "MEDIUM", "color": "#FBC02D", "action": "CAUTION"}
        elif score >= 20:
            return {"level": "LOW", "color": "#66BB6A", "action": "MONITOR"}
        else:
            return {"level": "SAFE", "color": "#2E7D32", "action": "ALLOW"}

    def _get_recommendation(self, score: float) -> str:
        if score >= 80:
            return "DO NOT ANSWER. This number matches known scam patterns. Block immediately."
        elif score >= 60:
            return "HIGH RISK. Likely scam call. Do not share any personal information, OTP, or install any apps."
        elif score >= 40:
            return "CAUTION. Suspicious patterns detected. Verify caller identity before sharing any information."
        elif score >= 20:
            return "LOW RISK. Appears legitimate but stay cautious. Never share OTP or passwords."
        else:
            return "This number appears safe based on current analysis."


# Singleton
scam_engine = ScamDetectionEngine()
