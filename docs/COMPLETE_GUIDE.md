# Complete Guide: Build & Publish SurakshaShield Android App

## What You Need to Install

### 1. Android Studio (FREE)
Download: https://developer.android.com/studio
- Size: ~1.5 GB
- Install and open it
- Follow the Setup Wizard
- Install SDK 34 when prompted

### 2. VS Code Extensions
Install these in VS Code:
- Kotlin (by fwcd)
- Python (by Microsoft)

---

## STEP-BY-STEP: Create the Project

### Step 1: Open Android Studio
```
1. Open Android Studio
2. Click "New Project"
3. Select "Empty Activity"
4. Click "Next"
5. Fill in:
   - Name: SurakshaShield
   - Package name: com.surakshashield
   - Save location: C:\Users\jiyad\OneDrive\Documents\Default Project\SurakshaShield\android
   - Language: Kotlin
   - Minimum SDK: API 26 (Android 8.0)
6. Click "Finish"
7. Wait for Gradle sync (5-10 minutes)
```

### Step 2: Open Project in VS Code
```
1. Open VS Code
2. File → Open Folder
3. Select: SurakshaShield\android
4. Click "Select Folder"
```

### Step 3: Copy All Code Files
I'll give you ALL the files below. Copy each one to the correct location.

### Step 4: Build the App
```
In Android Studio:
1. Click Build → Build Bundle(s) / APK(s) → Build APK(s)
2. Wait for build to complete
3. Click "locate" to find the APK
```

### Step 5: Install on Phone
```
1. Enable USB Debugging on your phone:
   - Settings → About Phone → Tap "Build Number" 7 times
   - Settings → Developer Options → Enable "USB Debugging"
2. Connect phone via USB
3. Click Run (▶️) in Android Studio
4. Select your phone
5. App will install automatically
```

### Step 6: Publish to Play Store
```
1. In Android Studio: Build → Generate Signed Bundle / APK
2. Select "Android App Bundle"
3. Create a new keystore (first time only)
4. Fill in details
5. Click "Create"
6. Upload to Google Play Console: https://play.google.com/console
```

---

## ALL CODE FILES (Copy These)

### File 1: build.gradle.kts (Project level)
Location: android/build.gradle.kts
```
See: SurakshaShield/android/build.gradle.kts
```

### File 2: build.gradle.kts (App level)
Location: android/app/build.gradle.kts
```
See: SurakshaShield/android/app/build.gradle.kts
```

### File 3: AndroidManifest.xml
Location: android/app/src/main/AndroidManifest.xml
```
See: SurakshaShield/android/app/src/main/AndroidManifest.xml
```

### File 4: MainActivity.kt
Location: android/app/src/main/java/com/surakshashield/MainActivity.kt
```
See: SurakshaShield/android/app/src/main/java/com/surakshashield/MainActivity.kt
```

... (and so on for all files)
```

---

## Quick Test (Before Publishing)

### Test on Emulator
```
1. In Android Studio: Tools → AVD Manager
2. Click "Create Virtual Device"
3. Select "Pixel 6" → Next
4. Download API 34 → Next
5. Click "Finish"
6. Click Run (▶️)
```

### Test on Real Phone
```
1. Connect phone via USB
2. Enable USB Debugging
3. Click Run (▶️)
4. Select your phone
```

---

## Common Issues & Fixes

### Issue: "Gradle sync failed"
```
Fix: File → Invalidate Caches → Restart
```

### Issue: "SDK not found"
```
Fix: File → Project Structure → SDK Location
Set path to: C:\Users\<username>\AppData\Local\Android\Sdk
```

### Issue: "Build failed"
```
Fix: Build → Clean Project → Rebuild Project
```

### Issue: "App not installing"
```
Fix: Uninstall old version first, then install new
```

---

## Need Help?

1. Follow this guide step by step
2. Copy ALL code files exactly as shown
3. Don't skip any steps
4. If stuck, search error on Google

**You can do this! 🚀**
