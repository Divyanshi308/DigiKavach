# How to Run DigiKavach on Your Phone (Demo)

## Method 1: Web Demo on Phone (EASIEST - Do this)

### Step 1: Get Your Netlify URL
- You already deployed to Netlify
- Your URL is like: https://something.netlify.app
- Open this URL on your phone's Chrome browser

### Step 2: Add to Home Screen (Makes it look like an app)
1. Open the Netlify URL in Chrome on your phone
2. Tap the **3 dots** (top right) → **Add to Home Screen**
3. Name it "DigiKavach" → Tap **Add**
4. Now it looks like a real app on your home screen!

### Step 3: Test the Features
1. **Scanner** - Tap Scanner tab → Enter `+919876543210` → See AI result
2. **Explainable AI** - Scroll down → Enter any number → See "Why?" breakdown
3. **WhatsApp Check** - Scroll to WhatsApp section → Paste scam message
4. **QR Generator** - Scroll to QR section → Generate UPI QR code
5. **Fraud Prediction** - Scroll to Prediction section → See 7-day forecast
6. **Dashboard** - Scroll to bottom → See live charts + 3D globe

---

## Method 2: Android APK on Phone (Real Android App)

### Step 1: Enable Developer Options
1. Open **Settings** on your phone
2. Go to **About Phone**
3. Tap **Build Number** 7 times
4. You'll see "You are now a developer"

### Step 2: Enable USB Debugging
1. Go to **Settings** → **Developer Options**
2. Turn on **USB Debugging**
3. Turn on **Install from Unknown Sources** (for APK install)

### Step 3: Transfer APK to Phone
**Option A: USB Cable**
1. Connect phone to laptop via USB cable
2. Open File Explorer → Find your phone
3. Copy `android\app\build\outputs\apk\debug\app-debug.apk` to phone's Downloads folder

**Option B: WhatsApp/Telegram**
1. Open WhatsApp Web on laptop
2. Send the APK file to yourself
3. Open WhatsApp on phone → Download the file

**Option C: Email**
1. Email the APK to yourself
2. Open email on phone → Download attachment

### Step 4: Install APK
1. Open **File Manager** on phone
2. Go to **Downloads** folder
3. Tap **app-debug.apk**
4. Tap **Install** (if asked "Allow from this source?" → Tap Allow)
5. App installed! Open "DigiKavach"

### Step 5: App Setup
1. Open DigiKavach app
2. Grant permissions when asked:
   - Phone permission (for call blocking)
   - SMS permission (for guardian alerts)
   - Contact permission (for emergency contacts)
3. App is ready!

---

## Method 3: Backend API Demo (For Technical Judges)

### Start Backend on Laptop
```powershell
cd "C:\Users\jiyad\OneDrive\Documents\Default Project\SurakshaShield\backend"
python -m app.main
```

### Show API Docs on Phone
1. Make sure laptop and phone are on **same WiFi**
2. Find laptop's IP: Open terminal → type `ipconfig`
3. On phone browser, go to: `http://YOUR-LAPTOP-IP:8000/docs`
4. This shows the interactive API documentation!
5. Tap any endpoint → Try it out → Show judges the real API

---

## Demo Flow for Judges (3 Minutes)

### For Web Demo (Recommended):
1. **0:00-0:10** - Open app → Onboarding tutorial plays
2. **0:10-0:30** - Scanner → Check scam number → Show result
3. **0:30-0:50** - Explainable AI → Show why it's a scam (signals breakdown)
4. **0:50-1:10** - WhatsApp checker → Paste scam message → AI verdict
5. **1:10-1:30** - QR Generator → Generate UPI QR → Show verification
6. **1:30-1:50** - Fraud Prediction → Show 7-day forecast + threats
7. **1:50-2:10** - Dashboard → 3D globe, 4 charts, live stats
8. **2:10-2:30** - Show API docs on phone (technical depth)
9. **2:30-3:00** - Close: "DigiKavach. 42 endpoints. 10 languages. Built for India."

### For Android App:
1. Same flow but using the native Android app
2. Show call blocking notification
3. Show settings with all toggles
4. Show language switch (Hindi/English)

---

## Quick Test Commands

### Test Scam Number:
- `+919876543210` → HIGH RISK
- `+911234567890` → DANGER
- `+919999999999` → CAUTION

### Test Loan App:
- `LoanOrbit` → SCAM (not in RBI list)
- `QuickCash` → DANGER
- `PhonePe` → SAFE

### Test Website:
- `fakebank.com` → PHISHING
- `phishingsite.com` → DANGER
- `google.com` → SAFE

### Test WhatsApp Message:
- "URGENT: Your account will be suspended. Click here to verify immediately" → SCAM
- "Congratulations! You won 10 lakh rupees. Click to claim" → SCAM
- "Meeting tomorrow at 10am" → SAFE

### Test Explainable AI:
- Enter any of the above → See full signal breakdown with weights

---

## Troubleshooting

### If web demo doesn't load:
- Make sure you have internet
- Try refreshing the page
- Check if Netlify URL is correct

### If Android app crashes:
- Make sure Android 8.0+ (API 26+)
- Uninstall and reinstall APK
- Check if storage space available

### If backend API doesn't respond:
- Make sure laptop and phone on same WiFi
- Check firewall isn't blocking port 8000
- Try using laptop IP instead of localhost
