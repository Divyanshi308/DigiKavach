# Complete VS Code Setup Guide for DigiKavach

## Step 1: Install Required Extensions

Open VS Code and install these extensions:

```
1. Kotlin (by fwcd)
2. Python (by Microsoft)
3. SQLite Viewer
4. Gradle for Java
5. Android iOS Support (by coder)
6. Code Runner
```

**How to install:**
1. Press `Ctrl+Shift+X` to open Extensions
2. Search for each extension
3. Click "Install"

---

## Step 2: Open Project in VS Code

```
1. Open VS Code
2. File → Open Folder
3. Navigate to: C:\Users\jiyad\OneDrive\Documents\Default Project\DigiKavach
4. Click "Select Folder"
```

---

## Step 3: Setup Backend (Python FastAPI)

### 3.1 Open Terminal
```
Press Ctrl + ` (backtick) to open terminal
```

### 3.2 Navigate to Backend
```bash
cd backend
```

### 3.3 Create Virtual Environment
```bash
python -m venv venv
```

### 3.4 Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# You should see (venv) in terminal
```

### 3.5 Install Dependencies
```bash
pip install -r requirements.txt
```

### 3.6 Start Backend Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3.7 Verify Backend is Running
```
Open browser: http://localhost:8000/health
You should see: {"status":"healthy","app":"DigiKavach","version":"1.0.0"}
```

---

## Step 4: Setup Android App

### 4.1 Open Android Folder
```
1. File → Open Folder
2. Navigate to: DigiKavach/android
3. Click "Select Folder"
```

### 4.2 Install Android SDK (if not installed)
```
1. Download Android Studio: https://developer.android.com/studio
2. Install and open Android Studio
3. SDK Manager → Install SDK 34
4. Note SDK path (usually C:\Users\<username>\AppData\Local\Android\Sdk)
```

### 4.3 Create local.properties
Create file `android/local.properties`:
```properties
sdk.dir=C\:\\Users\\jiyad\\AppData\\Local\\Android\\Sdk
```

### 4.4 Build Android App

**Option A: Using VS Code Terminal**
```bash
cd android
.\gradlew.bat assembleDebug
```

**Option B: Using Android Studio**
```
1. Open Android Studio
2. File → Open → Select android folder
3. Wait for Gradle sync
4. Click Run (▶️)
```

### 4.5 Run on Device/Emulator
```
1. Connect Android device via USB (enable USB debugging)
   OR
2. Start Android Emulator (Android Studio → Tools → AVD Manager)
3. In VS Code: Run → Start Debugging
4. Select your device
```

---

## Step 5: Test the Application

### 5.1 Test Backend API

Open new terminal (Ctrl + `):
```bash
# Health check
curl http://localhost:8000/health

# Check a phone number
curl "http://localhost:8000/api/v1/numbers/check?number=+919876543210"

# Check a loan app
curl "http://localhost:8000/api/v1/apps/check?name=KreditBee"

# Check a website
curl "http://localhost:8000/api/v1/websites/check?url=fakekredit.com"

# Get scam list
curl "http://localhost:8000/api/v1/numbers/scam-list"
```

### 5.2 Test Android App
```
1. Open app on device/emulator
2. Grant all permissions when prompted
3. Tap "Check Number" and enter: +919876543210
4. You should see "SCAM" warning
5. Tap "Verify App" and enter: KreditBee
6. You should see "SAFE" result
```

---

## Step 6: Debug in VS Code

### 6.1 Debug Backend
```
1. Open backend/app/main.py
2. Set breakpoint (click line number)
3. Press F5 or Run → Start Debugging
4. Select "Python: FastAPI"
```

### 6.2 Debug Android
```
1. Open any Kotlin file
2. Set breakpoint
3. Press F5 or Run → Start Debugging
4. Select "Android App"
```

---

## Step 7: Useful VS Code Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + `` | Toggle Terminal |
| `Ctrl + Shift + P` | Command Palette |
| `Ctrl + P` | Quick Open File |
| `F5` | Start Debugging |
| `Ctrl + Shift + F` | Search in Files |
| `Ctrl + /` | Comment/Uncomment |

---

## Troubleshooting

### Issue: "Python not found"
**Solution:**
```bash
# Add Python to PATH or use full path
C:\Users\jiyad\AppData\Local\Programs\Python\Python311\python.exe -m venv venv
```

### Issue: "Gradle sync failed"
**Solution:**
```
1. File → Invalidate Caches → Restart
2. Delete android/.gradle folder
3. Reopen project
```

### Issue: "Cannot find SDK"
**Solution:**
```
1. Open Android Studio
2. File → Project Structure → SDK Location
3. Copy SDK path
4. Update android/local.properties
```

### Issue: "Backend connection refused"
**Solution:**
```bash
# Make sure backend is running
cd backend
uvicorn app.main:app --reload --port 8000

# Check if port is in use
netstat -ano | findstr :8000
```

### Issue: "Permission denied on Android"
**Solution:**
```
1. Phone Settings → Apps → DigiKavach
2. Permissions → Enable all
3. Phone Settings → Apps → Default Apps → Phone App → Select DigiKavach
```

---

## Project Structure in VS Code

```
DigiKavach/
├── README.md                    # Project overview
├── docs/
│   └── SETUP.md                # Original setup guide
├── android/                    # Android app
│   ├── app/
│   │   ├── build.gradle.kts   # App dependencies
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       ├── java/com/digikavach/
│   │       │   ├── MainActivity.kt
│   │       │   ├── DigiKavachApp.kt
│   │       │   ├── data/       # Database & models
│   │       │   ├── service/    # Call screening
│   │       │   ├── ui/         # UI screens
│   │       │   ├── utils/      # Utilities
│   │       │   └── receiver/   # Boot receiver
│   │       └── res/            # Resources
│   └── build.gradle.kts       # Project dependencies
├── backend/                    # Python backend
│   ├── app/
│   │   ├── main.py            # FastAPI entry
│   │   └── api/               # API routes
│   ├── requirements.txt       # Python packages
│   └── data/                  # Scam databases
└── scripts/                   # Build scripts
```

---

## Quick Start Summary

```bash
# 1. Open terminal in VS Code (Ctrl + `)

# 2. Setup backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# 3. Open new terminal (Ctrl + Shift + `)

# 4. Build Android
cd android
.\gradlew.bat assembleDebug

# 5. Run on device
# Connect Android device or start emulator
# Press F5 in VS Code
```

---

## Next Steps

1. **Test all features** on Android device
2. **Connect backend** to Android app
3. **Import scam databases** from DoT/RBI
4. **Add more UI polish**
5. **Prepare for hackathon presentation**

---

## Need Help?

- Check this guide first
- Review code comments
- Search error in Google
- Ask team lead

**Happy Coding! 🚀**
