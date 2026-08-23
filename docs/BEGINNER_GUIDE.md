# STEP-BY-STEP: Build DigiKavach (Beginner Guide)

## What You'll Build
A phone app that:
- Blocks scam calls automatically
- Shows if a loan app is safe or fake
- Checks websites for phishing
- Alerts your family if you're in danger

---

## STEP 1: Install Android Studio

### 1.1 Download Android Studio
```
1. Open Chrome browser
2. Go to: https://developer.android.com/studio
3. Click "Download Android Studio"
4. Save the file (about 1.5 GB)
5. Wait for download to finish
```

### 1.2 Install Android Studio
```
1. Double-click the downloaded file
2. Click "Next" through all screens
3. Click "Install"
4. Wait for installation (5-10 minutes)
5. Click "Finish"
6. Android Studio will open automatically
```

### 1.3 Setup Android Studio (First Time)
```
1. Click "Standard" installation
2. Click "Next" through all screens
3. Wait for SDK download (10-15 minutes)
4. Click "Finish"
```

---

## STEP 2: Create New Project

### 2.1 Open Android Studio
```
1. Open Android Studio
2. Click "New Project"
3. Select "Empty Activity"
4. Click "Next"
```

### 2.2 Fill Project Details
```
Name: DigiKavach
Package name: com.digikavach
Save location: C:\Users\jiyad\OneDrive\Documents\Default Project\DigiKavach\android
Language: Kotlin
Minimum SDK: API 26 (Android 8.0)
Click "Finish"
```

### 2.3 Wait for Build
```
1. Wait 5-10 minutes for Gradle to build
2. You'll see "BUILD SUCCESSFUL" at bottom
3. Don't close Android Studio yet
```

---

## STEP 3: Open in VS Code

### 3.1 Open VS Code
```
1. Open VS Code
2. Click File → Open Folder
3. Navigate to: C:\Users\jiyad\OneDrive\Documents\Default Project\DigiKavach\android
4. Click "Select Folder"
```

### 3.2 Install Extensions
```
1. Click Extensions icon (left sidebar)
2. Search "Kotlin" → Install
3. Search "Python" → Install
```

---

## STEP 4: Copy Code Files

### 4.1 Open Each File Location

**File 1: app/build.gradle.kts**
```
1. In VS Code, open: android/app/build.gradle.kts
2. Select ALL text (Ctrl+A)
3. Delete it
4. Copy the code from docs/CODE_FILES.md (File 1)
5. Paste (Ctrl+V)
6. Save (Ctrl+S)
```

**File 2: AndroidManifest.xml**
```
1. Open: android/app/src/main/AndroidManifest.xml
2. Select ALL → Delete
3. Copy File 2 from CODE_FILES.md
4. Paste → Save
```

**File 3: MainActivity.kt**
```
1. Open: android/app/src/main/java/com/digikavach/MainActivity.kt
2. Select ALL → Delete
3. Copy File 3 from CODE_FILES.md
4. Paste → Save
```

**File 4: SurakshaCallScreeningService.kt**
```
1. Create folder: android/app/src/main/java/com/digikavach/service/
2. Create file: SurakshaCallScreeningService.kt
3. Copy File 4 from CODE_FILES.md
4. Paste → Save
```

**File 5: strings.xml**
```
1. Open: android/app/src/main/res/values/strings.xml
2. Select ALL → Delete
3. Copy File 5 from CODE_FILES.md
4. Paste → Save
```

**File 6: themes.xml**
```
1. Open: android/app/src/main/res/values/themes.xml
2. Select ALL → Delete
3. Copy File 6 from CODE_FILES.md
4. Paste → Save
```

---

## STEP 5: Build the App

### 5.1 Build in Android Studio
```
1. Switch to Android Studio
2. Click Build → Build Bundle(s) / APK(s) → Build APK(s)
3. Wait for build (2-3 minutes)
4. Click "locate" when done
5. You'll see the APK file
```

### 5.2 Build in VS Code (Alternative)
```
1. Open terminal in VS Code (Ctrl + `)
2. Type: cd android
3. Type: .\gradlew.bat assembleDebug
4. Wait for build
5. APK will be in: android/app/build/outputs/apk/debug/
```

---

## STEP 6: Install on Phone

### 6.1 Enable USB Debugging
```
1. On your phone, go to Settings
2. Go to About Phone
3. Tap "Build Number" 7 times
4. Go back to Settings → Developer Options
5. Enable "USB Debugging"
```

### 6.2 Connect Phone
```
1. Connect phone to computer via USB
2. On phone, tap "Allow USB Debugging"
3. In Android Studio, click Run (▶️)
4. Select your phone from the list
5. Wait for app to install
6. App will open automatically!
```

---

## STEP 7: Test the App

### 7.1 Test Phone Number Check
```
1. Open the app
2. Tap "Scanner" tab
3. Select "Phone"
4. Enter: +919876543210
5. Tap "CHECK NOW"
6. You should see "SCAM NUMBER DETECTED!"
```

### 7.2 Test Loan App Check
```
1. Tap "App" chip
2. Enter: LoanOrbit
3. Tap "CHECK NOW"
4. You should see "FRAUDULENT APP!"
```

### 7.3 Test Safe App
```
1. Clear the field
2. Enter: KreditBee
3. Tap "CHECK NOW"
4. You should see "LEGITIMATE APP"
```

---

## STEP 8: Test Backend API

### 8.1 Start Backend
```
1. Open new terminal in VS Code
2. Type: cd backend
3. Type: .\venv\Scripts\activate
4. Type: uvicorn app.main:app --reload
5. Wait for "Application startup complete"
```

### 8.2 Test API
```
Open browser and go to: http://localhost:8000/docs
You'll see the API documentation page
```

---

## STEP 9: Publish to Play Store

### 9.1 Create Play Store Account
```
1. Go to: https://play.google.com/console
2. Sign in with Google account
3. Pay $25 (one-time fee)
4. Complete account setup
```

### 9.2 Generate Signed APK
```
1. In Android Studio: Build → Generate Signed Bundle / APK
2. Select "Android App Bundle"
3. Click "Next"
4. Click "Create new" (first time)
5. Fill in:
   - Key store path: Choose a location
   - Password: Create a password
   - Key alias: digikavach
   - Key password: Create a password
   - Fill in certificate info
6. Click "OK"
7. Click "Next"
8. Select "release"
9. Click "Finish"
```

### 9.3 Upload to Play Store
```
1. Go to Google Play Console
2. Click "Create app"
3. Fill in app details:
   - App name: DigiKavach
   - Default language: English
   - App or game: App
   - Free
4. Complete content rating
5. Upload the AAB file from Step 9.2
6. Add screenshots and description
7. Click "Review and submit"
```

---

## Common Problems & Fixes

### Problem: "Gradle sync failed"
```
Fix: File → Invalidate Caches → Restart
```

### Problem: "SDK not found"
```
Fix: File → Project Structure → SDK Location
Set to: C:\Users\jiyad\AppData\Local\Android\Sdk
```

### Problem: "Build failed"
```
Fix: Build → Clean Project → Rebuild Project
```

### Problem: "App crashes on phone"
```
Fix: Check logcat in Android Studio for errors
```

### Problem: "Can't find Java"
```
Fix: Install Java 17:
  winget install Microsoft.OpenJDK.17
```

---

## You're Done! 🎉

Your app is now:
- ✅ Built
- ✅ Running on your phone
- ✅ Ready for Play Store

### Next Steps:
1. Add more scam numbers to the database
2. Improve the UI design
3. Add Hindi language support
4. Connect to real RBI database
5. Add WhatsApp bot feature

---

## Need Help?

1. Follow this guide exactly
2. Don't skip any steps
3. If stuck, search the error on Google
4. Ask your team for help

**You can do this! 🚀**
