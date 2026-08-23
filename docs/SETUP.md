# DigiKavach - Complete Setup Guide

## Prerequisites

### For Android Development
- Android Studio (latest version)
- JDK 17+
- Android SDK 34+
- Kotlin 1.9+

### For Backend Development
- Python 3.10+
- pip (Python package manager)
- PostgreSQL 14+
- Redis 7+

### For VS Code
- Kotlin extension
- Python extension
- SQLite Viewer extension

---

## Step 1: Clone/Setup Project

```bash
# Navigate to project folder
cd "C:\Users\jiyad\OneDrive\Documents\Default Project\DigiKavach"

# The project structure is already created
```

---

## Step 2: Setup Backend (Python FastAPI)

### 2.1 Create Virtual Environment
```bash
cd backend
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2.2 Install Dependencies
```bash
pip install -r requirements.txt
```

### 2.3 Setup Database
```bash
# Create PostgreSQL database
createdb digikavach

# Run migrations
python -m app.db.init
```

### 2.4 Start Backend Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be running at: `http://localhost:8000`
API Docs: `http://localhost:8000/docs`

---

## Step 3: Setup Android App

### 3.1 Open in Android Studio
```
1. Open Android Studio
2. File → Open
3. Navigate to: DigiKavach/android
4. Click OK
5. Wait for Gradle sync to complete
```

### 3.2 Configure SDK
```
1. File → Project Structure
2. SDK Location → Android SDK Location
3. Ensure SDK 34+ is installed
```

### 3.3 Add API Key
Create `local.properties` in android folder:
```properties
sdk.dir=C\:\\Users\\jiyad\\AppData\\Local\\Android\\Sdk
API_BASE_URL=http://10.0.2.2:8000
```

### 3.4 Build and Run
```
1. Select device/emulator
2. Click Run (▶️)
3. Wait for installation
```

---

## Step 4: Setup in VS Code

### 4.1 Open Project
```
1. Open VS Code
2. File → Open Folder
3. Select: DigiKavach
```

### 4.2 Install Extensions
```
1. Kotlin (by fwcd)
2. Python (by Microsoft)
3. SQLite Viewer
4. Gradle for Java
```

### 4.3 Run Backend from VS Code
```
1. Open terminal (Ctrl + `)
2. cd backend
3. .\venv\Scripts\activate  (Windows)
4. uvicorn app.main:app --reload
```

### 4.4 Open Android in VS Code
```
1. File → Open Folder → android
2. Use Kotlin extension for code completion
3. Build from terminal: .\gradlew.bat assembleDebug
```

---

## Step 5: Test the Application

### 5.1 Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# Check a phone number
curl http://localhost:8000/api/v1/check-number?number=+919876543210

# Check a loan app
curl http://localhost:8000/api/v1/check-loan-app?name=KreditBee
```

### 5.2 Test Android App
```
1. Install on device/emulator
2. Grant permissions when prompted
3. Test call screening with test numbers
4. Test loan app verification
```

---

## Step 6: Database Setup (Optional - For Full Features)

### 6.1 Import Scam Numbers
```bash
# Download DoT MNRL data (when available)
python scripts/import_mnrl.py

# Import I4C suspect registry
python scripts/import_i4c.py

# Import RBI fraud list
python scripts/import_rbi.py
```

### 6.2 Setup Redis Cache
```bash
# Start Redis
redis-server

# Or with Docker
docker run -d -p 6379:6379 redis:alpine
```

---

## Troubleshooting

### Common Issues

**Gradle Sync Failed**
```
Solution: File → Invalidate Caches → Restart
```

**Backend Connection Error**
```
Solution: Ensure backend is running on port 8000
Check: http://localhost:8000/health
```

**Permission Denied on Android**
```
Solution: 
1. Settings → Apps → DigiKavach
2. Grant all permissions
3. Set as default dialer
```

**Database Connection Error**
```
Solution:
1. Ensure PostgreSQL is running
2. Check credentials in config.py
3. Run: python -m app.db.init
```

---

## Project Structure

```
DigiKavach/
├── README.md                    # Project overview
├── docs/
│   └── SETUP.md                # This file
├── android/                    # Android app
│   ├── app/
│   │   └── src/main/
│   │       ├── java/com/digikavach/
│   │       │   ├── MainActivity.kt
│   │       │   ├── ui/          # UI components
│   │       │   ├── service/     # Call screening service
│   │       │   ├── data/        # Database & API
│   │       │   └── utils/       # Utilities
│   │       └── AndroidManifest.xml
│   └── build.gradle.kts
├── backend/                    # Python backend
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── api/               # API routes
│   │   ├── models/            # Database models
│   │   ├── services/          # Business logic
│   │   └── db/                # Database setup
│   ├── data/                  # Scam databases
│   ├── scripts/               # Utility scripts
│   └── requirements.txt
└── scripts/                   # Build & deploy scripts
```

---

## Next Steps

1. **Phase 1 (MVP)**: Basic call screening + loan app verification
2. **Phase 2**: Payment protection + guardian alerts
3. **Phase 3**: Full backend integration + database sync

---

## Support

For issues or questions:
- Check this SETUP.md first
- Review code comments
- Contact team lead

**Happy Coding! 🚀**
