# SurakshaShield - Pitch Deck Content
## Build$Bank FinTech Hackathon @ IIT Delhi

---

## SLIDE 1: Title Slide

### SurakshaShield
**Complete Fraud Protection for 424 Million UPI Users**

*From Scam Calls to Scam Apps - One Shield, Total Protection*

Team: [Your Team Name]
Members: [Names]
Date: September 20, 2026

---

## SLIDE 2: The Problem

### India's Fraud Crisis is Growing

| Stat | Data |
|------|------|
| Fake loan apps blocked | 3,718 |
| Money saved from fraud | ₹11,158 Crore |
| Complaints filed | 32.80 Lakh |
| Kerala complaints alone | 15,000 in 3 years |
| Suicides linked to loan scams | 7 |
| Monthly UPI fraud cases | 95,000+ |

**Root Cause:** Users have NO easy way to verify if a caller, app, or website is legitimate BEFORE it's too late.

---

## SLIDE 3: The Gap

### Current Solutions Fall Short

| Existing Solution | Limitation |
|------------------|------------|
| RBI DLA Directory | Unknown to 95% users, hard to navigate |
| S.A.F.E. Test | Manual, requires financial literacy |
| Google Play Store | Fake apps slip through |
| I4C blocking | Reactive, not preventive |
| Truecaller | Only identifies callers, doesn't block |
| Arjuna Cyber Shield | No government database integration |

**The Gap:** No app provides COMPLETE protection - from call to payment.

---

## SLIDE 4: Our Solution

### SurakshaShield: Complete Protection

**"We don't just warn you. We protect you."**

```
Layer 1: BLOCK    → Scam calls automatically
Layer 2: IDENTIFY → Real-time caller ID & risk score
Layer 3: PROTECT  → Payment protection during calls
Layer 4: VERIFY   → Loan app & website checking
Layer 5: ALERT    → Guardian notifications
```

**One app. Complete protection. Before, during, and after.**

---

## SLIDE 5: How It Works

### 4-Layer Protection System

**Layer 1: Call Blocking**
- Integrates with DoT MNRL (Mobile Number Revocation List)
- Checks I4C Suspect Registry (30.48 lakh records)
- Auto-blocks known scam numbers
- Uses Android CallScreeningService API

**Layer 2: Real-time Caller ID**
- Shows risk score before answering
- Displays scam type (digital arrest, loan fraud, etc.)
- Color-coded warnings: Green → Yellow → Orange → Red

**Layer 3: Payment Protection**
- Detects when banking app opened during unknown call
- Shows full-screen warning overlay
- Sends guardian SMS alert
- Monitors UPI apps (GPay, PhonePe, Paytm, etc.)

**Layer 4: Verification Tools**
- Phone number checker
- Loan app verifier (RBI directory)
- Website phishing detector
- UPI QR code scanner

---

## SLIDE 6: Live Demo

### Watch It Work

**Demo 1: Scam Call Blocking**
```
1. Incoming call from +919876543210 (known scam number)
2. App shows: "SCAM CALL BLOCKED!" in red
3. Call is automatically rejected
4. User sees risk score: 95/100
```

**Demo 2: Loan App Verification**
```
1. User enters "LoanOrbit"
2. App shows: "FRAUDULENT APP" in red
3. Details: Blocked by I4C on Aug 7, 2026
4. Reason: Exorbitant interest rates, data harvesting
```

**Demo 3: Safe App Verification**
```
1. User enters "KreditBee"
2. App shows: "LEGITIMATE APP" in green
3. Details: RBI Registered, NBFC verified
4. Risk Score: 15/100
```

**Demo 4: Payment Protection**
```
1. User on call with unknown number
2. Opens Google Pay
3. App shows warning: "STOP! You're on a suspicious call!"
4. Guardian receives SMS alert
```

---

## SLIDE 7: Technology

### Built with Modern Tech Stack

**Android App (Kotlin + Jetpack Compose)**
- CallScreeningService API (Android 10+)
- Material Design 3 UI
- Local database (Room)
- Foreground services

**Backend API (Python FastAPI)**
- REST API endpoints
- Scam number database
- Loan app verification
- Website checking

**Data Sources**
- DoT MNRL (Mobile Number Revocation List)
- RBI Digital Lending Apps Directory
- I4C Suspect Registry
- Cybercrime.gov.in reports
- Community crowdsourcing

---

## SLIDE 8: Market Opportunity

### 424 Million Users Need Protection

| Market | Size |
|--------|------|
| UPI users in India | 424 Million |
| Monthly UPI transactions | 16 Billion |
| Annual digital fraud | ₹22,495 Crore |
| Growing at | 24% YoY |

**Our Target Users:**
- Elderly parents (fraud targets)
- First-time digital users
- Rural/semi-urban populations
- Small business owners
- Students

---

## SLIDE 9: Business Model

### Sustainable Revenue Streams

**Freemium Model**
- Free: Basic call blocking + number checking
- Premium: Full protection suite (₹99/month)

**B2B Revenue**
- API access for banks/NBFCs
- Analytics dashboard for regulators
- White-label solution for telecoms

**Partnerships**
- RBI (official data access)
- NPCI (UPI integration)
- Banks (co-branding)
- Insurance companies (fraud protection)

---

## SLIDE 10: Traction & Roadmap

### What We've Built

**MVP Complete:**
- Android app with call screening
- Backend API with 6 endpoints
- Scam number database
- Loan app verification
- Website checking

**Roadmap:**
| Phase | Timeline | Features |
|-------|----------|----------|
| MVP | Done | Call blocking + verification |
| V1.0 | Oct 2026 | WhatsApp bot + guardian alerts |
| V2.0 | Dec 2026 | Bank partnerships + NPCI integration |
| V3.0 | Mar 2027 | AI-powered scam detection |

---

## SLIDE 11: Team

### Meet the Team

[Your Name] - [Role]
[Member 2] - [Role]
[Member 3] - [Role]
[Member 4] - [Role]

**Skills:**
- Android Development (Kotlin)
- Backend Development (Python)
- UI/UX Design
- Data Analysis
- Financial Domain Knowledge

---

## SLIDE 12: Ask

### What We Need

**To Execute:**
- Mentorship from fintech experts
- Access to RBI/DoT data APIs
- Cloud infrastructure for backend
- Beta testers for feedback

**To Scale:**
- Bank partnership introductions
- Play Store featured spot
- Media coverage

**Contact:**
- Email: [your email]
- GitHub: [repo link]
- Demo: [live demo link]

---

## APPENDIX: Key Differentiators

| Feature | Us | Truecaller | Arjuna | ScamMukt |
|---------|-----|-----------|--------|----------|
| Auto-block scam calls | ✅ | ❌ | ❌ | ❌ |
| RBI database integration | ✅ | ❌ | Partial | ❌ |
| Payment protection | ✅ | ❌ | ❌ | ❌ |
| Guardian alerts | ✅ | ❌ | ❌ | ❌ |
| Loan app verification | ✅ | ❌ | ❌ | Partial |
| Website checking | ✅ | ❌ | ✅ | ✅ |
| UPI QR scanning | ✅ | ❌ | ✅ | ✅ |

**We are the ONLY app with COMPLETE protection.**
