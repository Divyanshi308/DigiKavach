# 🛡️ DigiKavach

**Complete Fraud Protection for 424 Million UPI Users**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Android](https://img.shields.io/badge/Platform-Android-green.svg)](https://developer.android.com)
[![Python](https://img.shields.io/badge/Backend-Python-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/API-FastAPI-red.svg)](https://fastapi.tiangolo.com)

---

## 📱 Features

| Feature | Description |
|---------|-------------|
| 🚫 **Call Blocking** | Auto-block scam calls using DoT MNRL database |
| 📞 **Real-time Caller ID** | Show risk score before answering |
| 💳 **Payment Protection** | Alert when banking app opened during unknown call |
| 🔍 **Loan App Verification** | Check apps against RBI directory |
| 🌐 **Website Checking** | Detect phishing websites |
| 📱 **UPI QR Scanner** | Verify UPI IDs before payment |
| 👨‍👩‍👧 **Guardian Alerts** | SMS alerts to emergency contacts |

---

## 🏗️ Architecture

```
DigiKavach/
├── android/          # Android app (Kotlin + Jetpack Compose)
│   ├── app/
│   │   └── src/main/
│   │       ├── java/com/digikavach/
│   │       │   ├── MainActivity.kt
│   │       │   ├── service/
│   │       │   │   └── SurakshaCallScreeningService.kt
│   │       │   └── ui/
│   │       │       └── screens/
│   │       └── AndroidManifest.xml
│   └── build.gradle.kts
├── backend/          # Python FastAPI backend
│   ├── app/
│   │   ├── main.py
│   │   └── api/
│   │       ├── numbers.py
│   │       ├── apps.py
│   │       ├── websites.py
│   │       └── alerts.py
│   └── requirements.txt
├── docs/             # Documentation
│   ├── PITCH_DECK.md
│   ├── DEMO_VIDEO_SCRIPT.md
│   └── BEGINNER_GUIDE.md
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites
- Android Studio (latest)
- Python 3.10+
- Java 17+

### Backend Setup
```bash
# Clone the repo
git clone https://github.com/yourusername/DigiKavach.git
cd DigiKavach/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload
```

### Android Setup
```bash
# Open Android Studio
# File → Open → Select android/ folder
# Wait for Gradle sync
# Click Run (▶️)
```

### Test API
```bash
# Health check
curl http://localhost:8000/health

# Check phone number
curl "http://localhost:8000/api/v1/numbers/check?number=+919876543210"

# Check loan app
curl "http://localhost:8000/api/v1/apps/check?name=KreditBee"
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/api/v1/numbers/check` | GET | Check phone number |
| `/api/v1/numbers/report` | POST | Report scam number |
| `/api/v1/numbers/scam-list` | GET | Get scam numbers |
| `/api/v1/apps/check` | GET | Check loan app |
| `/api/v1/apps/search` | GET | Search loan apps |
| `/api/v1/apps/rbi-directory` | GET | Get RBI directory |
| `/api/v1/websites/check` | GET | Check website |
| `/api/v1/websites/check-qr` | GET | Check UPI QR |
| `/api/v1/alerts/setup-guardian` | POST | Setup guardian |
| `/api/v1/alerts/send-alert` | POST | Send alert |

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Mobile** | Kotlin, Jetpack Compose, Material 3 |
| **Backend** | Python, FastAPI, Pydantic |
| **Database** | SQLite (local), PostgreSQL (production) |
| **APIs** | DoT MNRL, RBI DLA Directory, I4C Registry |
| **Architecture** | MVVM, Clean Architecture |

---

## 📊 Data Sources

| Source | Description |
|--------|-------------|
| **DoT MNRL** | Mobile Number Revocation List |
| **RBI DLA Directory** | 1,600+ legitimate lending apps |
| **I4C Suspect Registry** | 30.48 lakh suspect identifiers |
| **Cybercrime.gov.in** | Fraud reports and complaints |
| **Community Reports** | User-submitted scam reports |

---

## 🎯 Problem Statement

> **PS23: Verifying Legitimate Lenders**
> 
> Find a way to help someone tell a genuine loan app or lender apart from a fraudulent one before they hand over money or documents.

### Our Approach

We go beyond verification - we provide **complete protection**:

1. **BLOCK** - Scam calls automatically
2. **IDENTIFY** - Real-time caller ID & risk score
3. **PROTECT** - Payment protection during calls
4. **VERIFY** - Loan app & website checking
5. **ALERT** - Guardian notifications

---

## 📈 Impact Numbers

| Metric | Value |
|--------|-------|
| Fake apps blocked (Govt) | 3,718 |
| Money saved from fraud | ₹11,158 Crore |
| Complaints filed | 32.80 Lakh |
| Monthly UPI fraud cases | 95,000+ |
| Our potential users | 424 Million |

---

## 🎬 Demo

### Live Demo
[Click here for live demo](https://your-demo-link.vercel.app)

### Video Demo
[Watch 3-minute demo video](https://youtube.com/your-video-link)

### Screenshots
| Home | Scanner | Alerts |
|------|---------|--------|
| ![Home](docs/screenshots/home.png) | ![Scanner](docs/screenshots/scanner.png) | ![Alerts](docs/screenshots/alerts.png) |

---

## 🛣️ Roadmap

| Phase | Timeline | Features |
|-------|----------|----------|
| **MVP** | Done | Call blocking + verification |
| **V1.0** | Oct 2026 | WhatsApp bot + guardian alerts |
| **V2.0** | Dec 2026 | Bank partnerships + NPCI integration |
| **V3.0** | Mar 2027 | AI-powered scam detection |

---

## 👥 Team

| Name | Role |
|------|------|
| [Your Name] | Lead Developer |
| [Member 2] | Backend Developer |
| [Member 3] | UI/UX Designer |
| [Member 4] | Data Analyst |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Reserve Bank of India (RBI) for DLA Directory
- Department of Telecommunications (DoT) for MNRL
- Indian Cyber Crime Coordination Centre (I4C) for suspect registry
- Build$Bank FinTech Hackathon @ IIT Delhi

---

## 📞 Contact

- **Email:** your.email@example.com
- **GitHub:** github.com/yourusername/DigiKavach
- **LinkedIn:** linkedin.com/in/yourprofile

---

**Built with ❤️ for Build$Bank FinTech Hackathon @ IIT Delhi**
