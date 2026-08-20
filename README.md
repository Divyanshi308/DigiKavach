# SurakshaShield - Complete Fraud Protection App

## Overview
SurakshaShield is a comprehensive fraud protection application that protects users from:
- **Scam Calls** - Auto-blocks known scam numbers
- **Fake Loan Apps** - Verifies lenders against RBI directory
- **Payment Fraud** - Detects suspicious transactions
- **Phishing Websites** - Blocks fraudulent sites

## Architecture
```
SurakshaShield/
├── android/          # Android app (Kotlin + Jetpack Compose)
├── backend/          # Python FastAPI backend
└── docs/             # Documentation
```

## Features
1. **Call Screening** - Blocks scam calls using DoT MNRL database
2. **Real-time Caller ID** - Shows scam risk before answering
3. **Payment Protection** - Alerts when banking app opened during unknown call
4. **Loan App Verifier** - Checks apps against RBI directory
5. **Website Scanner** - Verifies URLs for phishing
6. **Guardian Alerts** - SMS alerts to emergency contacts

## Tech Stack
- **Android**: Kotlin, Jetpack Compose, CallScreeningService API
- **Backend**: Python FastAPI, PostgreSQL, Redis
- **APIs**: DoT MNRL, RBI DLA Directory, I4C Suspect Registry

## Quick Start
See `docs/SETUP.md` for detailed instructions.
