"""
Vernacular Language Support - Hindi + Regional Indian Languages
Offline Scam Detection + Community Features
"""
from typing import Dict, List, Optional
import json
from pathlib import Path


class VernacularEngine:
    """
    Multi-language scam detection for India's diverse population.
    Supports: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam
    """

    # Hindi scam scripts (exact phrases scammers use)
    HINDI_SCAM_SCRIPTS = {
        "digital_arrest": [
            "आपका डिजिटल अरेस्ट हो गया है",
            "आप पर CBI का केस चल रहा है",
            "पुलिस स्टेशन से बोल रहे हैं",
            "वारंट जारी हो गया है आपके नाम पर",
            "आपका PAN कार्ड ब्लॉक हो गया है",
            "आपका अकाउंट फ्रीज कर दिया गया है",
            "ये आपकी आखिरी चेतावनी है",
            "तुरंत पुलिस स्टेशन आओ नहीं तो गिरफ्तारी होगी",
        ],
        "otp_phishing": [
            "OTP बताओ जल्दी से",
            "OTP शेयर करो अभी",
            "वेरिफिकेशन कोड भेजो",
            "मुझे OTP बता दो सिर्फ",
            "OTP नंबर बताओ तुरंत",
            "स्क्रीन शेयरिंग ऑन करो",
            "AnyDesk इंस्टॉल करो",
            "TeamViewer डाउनलोड करो",
        ],
        "loan_fraud": [
            "लोन अप्रूव हो गया है",
            "तुरंत लोन मिलेगा बिना डॉक्यूमेंट",
            "घर बैठे लोन पाओ",
            "90% डिस्काउंट पर लोन",
            "फ्री गिफ्ट मिलेगा",
            "आप लकी विनर हैं",
            "इन्वेस्ट करो 100% प्रॉफिट",
            "डबल पैसा होगा 7 दिन में",
        ],
        "kyc_fraud": [
            "KYC अपडेट करना है",
            "KYC वेरिफिकेशन पेंडिंग है",
            "आपका KYC बंद हो जाएगा",
            "KYC अपडेट नहीं किया तो अकाउंट बंद",
            "आधार अपडेट करना है",
            "पैन कार्ड अपडेट करो",
        ],
    }

    # Common scam English phrases used in India
    ENGLISH_SCAM_PHRASES = [
        "You are under digital arrest",
        "This is CBI speaking",
        "Your account will be frozen",
        "Share your OTP immediately",
        "Install AnyDesk for verification",
        "You have won a lottery",
        "Transfer money to this account",
        "Your KYC is expired",
        "Give me your screen access",
        "Don't tell anyone about this call",
    ]

    # Translation dictionary for scam warnings
    SCAM_WARNINGS = {
        "en": {
            "critical": "DANGER! This is a scam call!",
            "high": "WARNING! High risk of fraud",
            "medium": "CAUTION: Suspicious activity detected",
            "blocked": "This scam call has been BLOCKED",
            "guardian_alert": "Alert sent to your guardian",
            "report_scam": "Report this scam",
            "emergency": "Call 1930 (Cyber Crime Helpline)",
        },
        "hi": {
            "critical": "खतरा! यह घोटाले का कॉल है!",
            "high": "चेतावनी! धोखाधड़ी का उच्च जोखिम",
            "medium": "सावधान: संदिग्ध गतिविधि का पता चला",
            "blocked": "यह घोटाले का कॉल ब्लॉक कर दिया गया है",
            "guardian_alert": "आपके अभिभावक को अलर्ट भेजा गया",
            "report_scam": "इस घोटाले की रिपोर्ट करें",
            "emergency": "1930 पर कॉल करें (साइबर क्राइम हेल्पलाइन)",
        },
        "ta": {
            "critical": "ஆபத்து! இது மோசடி அழைப்பு!",
            "high": "எச்சரிக்கை! மோசடி அபாயம் அதிகம்",
            "medium": "கவனம்: சந்தேகமான நடவடிக்கை கண்டறியப்பட்டது",
            "blocked": "இந்த மோசடி அழைப்பு தடுக்கப்பட்டது",
            "guardian_alert": "உங்கள் பாதுகாவலருக்கு எச்சரிக்கை அனுப்பப்பட்டது",
            "report_scam": "இந்த மோசடியைப் புகாரளியுங்கள்",
            "emergency": "1930 அழைக்கவும் (சைபர் குற்ற உதவி எண்)",
        },
        "te": {
            "critical": "ప్రమాదం! ఇది మోసపు కాల్!",
            "high": "హెచ్చరిక! మోసం ప్రమాదం ఎక్కువ",
            "medium": "జాగ్రత్త: అనుమానాస్పద కార్యాచరణ గుర్తించబడింది",
            "blocked": "ఈ మోసపు కాల్ బ్లాక్ చేయబడింది",
            "guardian_alert": "మీ సంరక్షకుడికి హెచ్చరిక పంపబడింది",
            "report_scam": "ఈ మోసాన్ని నివేదించండి",
            "emergency": "1930 కి కాల్ చేయండి (సైబర్ క్రైమ్ హెల్ప్‌లైన్)",
        },
        "bn": {
            "critical": "বিপদ! এটি প্রতারণার কল!",
            "high": "সতর্কতা! প্রতারণার উচ্চ ঝুঁকি",
            "medium": "সাবধান: সন্দেহজনক কার্যকলাপ সনাক্ত",
            "blocked": "এই প্রতারণার কল ব্লক করা হয়েছে",
            "guardian_alert": "আপনার অভিভাবককে সতর্কতা পাঠানো হয়েছে",
            "report_scam": "এই প্রতারণার রিপোর্ট করুন",
            "emergency": "1930 এ কল করুন (সাইবার অপরাধ হেল্পলাইন)",
        },
        "mr": {
            "critical": "धोका! हा फसवणूकी कॉल आहे!",
            "high": "सूचना! फसवणूकीचा उच्च धोका",
            "medium": "सावधान: शंकास्पद क्रिया आढळली",
            "blocked": "हा फसवणूकी कॉल ब्लॉक केला आहे",
            "guardian_alert": "तुमच्या संरक्षकाला सूचना पाठवली",
            "report_scam": "या फसवणुकीचा तक्रार करा",
            "emergency": "1930 वर कॉल करा (सायबर गुन्हा हेल्पलाइन)",
        },
        "gu": {
            "critical": "ખતરો! આ છેતરપિંડીનો કૉલ છે!",
            "high": "ચેતવણી! છેતરપિંડીનું ઊંચું જોખમ",
            "medium": "સાવધાન: શંકાસ્પદ પ્રવૃત્તિ મળી",
            "blocked": "આ છેતરપિંડી કૉલ બ્લૉક થયો",
            "guardian_alert": "તમારા સંરક્ષકને ચેતવણી મોકલી",
            "report_scam": "આ છેતરપિંડીની ફરિયાદ કરો",
            "emergency": "1930 પર કૉલ કરો (સાયબર ક્રાઈમ હેલ્પલાઈન)",
        },
        "kn": {
            "critical": "ಅಪಾಯ! ಇದು ವಂಚನೆ ಕರೆ!",
            "high": "ಎಚ್ಚರಿಕೆ! ವಂಚನೆ ಅಪಾಯ ಹೆಚ್ಚು",
            "medium": "ಎಚ್ಚರಿಕೆ: ಅನುಮಾನಾಸ್ಪದ ಚಟುವಟಿಕೆ ಪತ್ತೆ",
            "blocked": "ಈ ವಂಚನೆ ಕರೆ ತಡೆಯಲಾಗಿದೆ",
            "guardian_alert": "ನಿಮ್ಮ ರಕ್ಷಕರಿಗೆ ಎಚ್ಚರಿಕೆ ಕಳುಹಿಸಲಾಗಿದೆ",
            "report_scam": "ಈ ವಂಚನೆಯನ್ನು ವರದಿ ಮಾಡಿ",
            "emergency": "1930 ಗೆ ಕರೆ ಮಾಡಿ (ಸೈಬರ್ ಅಪರಾಧ ಸಹಾಯವಾಣಿ)",
        },
        "ml": {
            "critical": "അപകടം! ഇത് തട്ടിപ്പ് കോൾ!",
            "high": "മുന്നറിയിപ്പ്! തട്ടിപ്പ് അപകടം കൂടുതൽ",
            "medium": "ശ്രദ്ധിക്കുക: സംശയാസ്പദ പ്രവർത്തനം കണ്ടെത്തി",
            "blocked": "ഈ തട്ടിപ്പ് കോൾ ബ്ലോക്ക് ചെയ്തു",
            "guardian_alert": "നിങ്ങളുടെ സംരക്ഷകന് മുന്നറിയിപ്പ് അയച്ചു",
            "report_scam": "ഈ തട്ടിപ്പ് റിപ്പോർട്ട് ചെയ്യുക",
            "emergency": "1930 ൽ വിളിക്കുക (സൈബർ കുറ്റകൃത്യ സഹായ ഹെൽപ്പ്‌ലൈൻ)",
        },
    }

    def detect_language(self, text: str) -> str:
        """Auto-detect the language of input text"""
        # Check for Devanagari (Hindi/Marathi)
        if any('\u0900' <= c <= '\u097F' for c in text):
            return "hi"
        # Check for Tamil
        if any('\u0B80' <= c <= '\u0BFF' for c in text):
            return "ta"
        # Check for Telugu
        if any('\u0C00' <= c <= '\u0C7F' for c in text):
            return "te"
        # Check for Bengali
        if any('\u0980' <= c <= '\u09FF' for c in text):
            return "bn"
        # Check for Gujarati
        if any('\u0A80' <= c <= '\u0AFF' for c in text):
            return "gu"
        # Check for Kannada
        if any('\u0C80' <= c <= '\u0CFF' for c in text):
            return "kn"
        # Check for Malayalam
        if any('\u0D00' <= c <= '\u0D7F' for c in text):
            return "ml"
        return "en"

    def check_hindi_scam_script(self, text: str) -> Dict:
        """Check if text matches known Hindi scam scripts"""
        text_lower = text.lower()
        matches = []

        for scam_type, phrases in self.HINDI_SCAM_SCRIPTS.items():
            for phrase in phrases:
                if phrase.lower() in text_lower:
                    matches.append({
                        "scam_type": scam_type,
                        "matched_phrase": phrase,
                        "confidence": 0.95,
                    })

        return {
            "matches": matches,
            "is_scam_script": len(matches) > 0,
            "scam_types_detected": list(set(m["scam_type"] for m in matches)),
        }

    def get_warning(self, language: str, severity: str) -> str:
        """Get localized scam warning"""
        lang_warnings = self.SCAM_WARNINGS.get(language, self.SCAM_WARNINGS["en"])
        return lang_warnings.get(severity, lang_warnings["critical"])

    def get_all_languages(self) -> List[Dict]:
        """Get list of supported languages"""
        return [
            {"code": "en", "name": "English", "native": "English"},
            {"code": "hi", "name": "Hindi", "native": "हिन्दी"},
            {"code": "ta", "name": "Tamil", "native": "தமிழ்"},
            {"code": "te", "name": "Telugu", "native": "తెలుగు"},
            {"code": "bn", "name": "Bengali", "native": "বাংলা"},
            {"code": "mr", "name": "Marathi", "native": "मराठी"},
            {"code": "gu", "name": "Gujarati", "native": "ગુજરાતી"},
            {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ"},
            {"code": "ml", "name": "Malayalam", "native": "മലയാളം"},
        ]


# ─── Offline Mode Engine ────────────────────────────────────────────

class OfflineEngine:
    """
    Offline scam detection for areas with no internet.
    Stores essential data locally on device.
    """

    def __init__(self):
        self.offline_db = {
            "scam_numbers": {},
            "phishing_domains": [],
            "scam_app_names": [],
            "scam_keywords_hindi": [],
            "scam_keywords_english": [],
            "emergency_numbers": {
                "cyber_crime": "1930",
                "police": "100",
                "women_helpline": "181",
                "ambulance": "108",
                "fire": "101",
            },
        }

    def get_offline_risk_score(self, phone: str, context: Dict = None) -> Dict:
        """Calculate risk score without internet"""
        score = 0
        factors = []

        # Local number pattern check
        clean = phone.replace("+91", "").strip()
        if clean.startswith("140"):
            score += 60
            factors.append("Telemarketing prefix detected")

        # Local scam number check
        if phone in self.offline_db["scam_numbers"]:
            score = 95
            factors.append("Number in local scam database")

        return {
            "risk_score": min(100, score),
            "offline_mode": True,
            "factors": factors,
            "emergency_number": "1930",
        }


# Singletons
vernacular_engine = VernacularEngine()
offline_engine = OfflineEngine()
