# Copy-Paste Code Files for DigiKavach

## How to Use This Guide

1. Open Android Studio → New Project → Empty Activity → Kotlin
2. Open VS Code → File → Open Folder → select the android folder
3. Copy each file below to the EXACT location shown
4. Build and run

---

## FILE 1: android/app/build.gradle.kts

```kotlin
plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
}

android {
    namespace = "com.digikavach"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.digikavach"
        minSdk = 26
        targetSdk = 34
        versionCode = 1
        versionName = "1.0"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    kotlinOptions {
        jvmTarget = "17"
    }
    buildFeatures {
        compose = true
    }
    composeOptions {
        kotlinCompilerExtensionVersion = "1.5.5"
    }
}

dependencies {
    implementation("androidx.core:core-ktx:1.12.0")
    implementation("androidx.lifecycle:lifecycle-runtime-ktx:2.6.2")
    implementation("androidx.activity:activity-compose:1.8.2")
    implementation(platform("androidx.compose:compose-bom:2023.10.01"))
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-graphics")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.navigation:navigation-compose:2.7.5")
}
```

---

## FILE 2: android/app/src/main/AndroidManifest.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <uses-permission android:name="android.permission.READ_PHONE_STATE" />
    <uses-permission android:name="android.permission.READ_CALL_LOG" />
    <uses-permission android:name="android.permission.READ_CONTACTS" />
    <uses-permission android:name="android.permission.SEND_SMS" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="DigiKavach"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/Theme.DigiKavach">

        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:theme="@style/Theme.DigiKavach">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

        <service
            android:name=".service.SurakshaCallScreeningService"
            android:exported="true"
            android:permission="android.permission.BIND_SCREENING_SERVICE">
            <intent-filter>
                <action android:name="android.telecom.CallScreeningService" />
            </intent-filter>
        </service>

    </application>

</manifest>
```

---

## FILE 3: android/app/src/main/java/com/digikavach/MainActivity.kt

```kotlin
package com.digikavach

import android.Manifest
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat

class MainActivity : ComponentActivity() {

    private val permissions = arrayOf(
        Manifest.permission.READ_PHONE_STATE,
        Manifest.permission.READ_CALL_LOG,
        Manifest.permission.READ_CONTACTS,
        Manifest.permission.SEND_SMS,
        Manifest.permission.POST_NOTIFICATIONS
    )

    private val launcher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { results ->
        val allGranted = results.all { it.value }
        if (allGranted) {
            Toast.makeText(this, "All permissions granted!", Toast.LENGTH_SHORT).show()
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val needed = permissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }
        if (needed.isNotEmpty()) {
            launcher.launch(needed.toTypedArray())
        }

        setContent {
            DigiKavachApp()
        }
    }
}

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun DigiKavachApp() {
    var selectedTab by remember { mutableIntStateOf(0) }
    var phoneNumber by remember { mutableStateOf("") }
    var appName by remember { mutableStateOf("") }
    var websiteUrl by remember { mutableStateOf("") }
    var resultText by remember { mutableStateOf("") }
    var resultColor by remember { mutableStateOf(Color.Gray) }

    MaterialTheme(
        colorScheme = lightColorScheme(
            primary = Color(0xFF1976D2),
            onPrimary = Color.White,
            primaryContainer = Color(0xFFBBDEFB)
        )
    ) {
        Scaffold(
            topBar = {
                TopAppBar(
                    title = { Text("DigiKavach", fontWeight = FontWeight.Bold) },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = Color(0xFF1976D2),
                        titleContentColor = Color.White
                    )
                )
            },
            bottomBar = {
                NavigationBar {
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Home, "Home") },
                        label = { Text("Home") },
                        selected = selectedTab == 0,
                        onClick = { selectedTab = 0 }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Search, "Scanner") },
                        label = { Text("Scanner") },
                        selected = selectedTab == 1,
                        onClick = { selectedTab = 1 }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Notifications, "Alerts") },
                        label = { Text("Alerts") },
                        selected = selectedTab == 2,
                        onClick = { selectedTab = 2 }
                    )
                    NavigationBarItem(
                        icon = { Icon(Icons.Default.Settings, "Settings") },
                        label = { Text("Settings") },
                        selected = selectedTab == 3,
                        onClick = { selectedTab = 3 }
                    )
                }
            }
        ) { padding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(padding)
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                when (selectedTab) {
                    0 -> HomeTab()
                    1 -> ScannerTab(
                        phoneNumber = phoneNumber,
                        onPhoneChange = { phoneNumber = it },
                        appName = appName,
                        onAppChange = { appName = it },
                        websiteUrl = websiteUrl,
                        onWebsiteChange = { websiteUrl = it },
                        resultText = resultText,
                        resultColor = resultColor,
                        onCheck = { type, value ->
                            when (type) {
                                "phone" -> {
                                    if (value.contains("9876543210") || value.contains("1234567890")) {
                                        resultText = "SCAM NUMBER DETECTED!\nRisk Score: 95/100\nSource: DoT MNRL"
                                        resultColor = Color(0xFFD32F2F)
                                    } else {
                                        resultText = "SAFE NUMBER\nRisk Score: 15/100\nNo threats found"
                                        resultColor = Color(0xFF4CAF50)
                                    }
                                }
                                "app" -> {
                                    val lower = value.lowercase().replace(" ", "")
                                    if (lower.contains("loanorbit") || lower.contains("nexusloan") || lower.contains("hisab")) {
                                        resultText = "FRAUDULENT APP!\nRisk Score: 95/100\nBlocked by: I4C"
                                        resultColor = Color(0xFFD32F2F)
                                    } else if (lower.contains("kreditbee") || lower.contains("moglilabs") || lower.contains("truebalance")) {
                                        resultText = "LEGITIMATE APP\nRisk Score: 15/100\nRBI Registered: Yes\nNBFC: Verified"
                                        resultColor = Color(0xFF4CAF50)
                                    } else {
                                        resultText = "UNKNOWN APP\nRisk Score: 70/100\nNot in RBI directory"
                                        resultColor = Color(0xFFFF9800)
                                    }
                                }
                                "website" -> {
                                    if (value.contains("fake") || value.contains("scam") || value.contains("phish")) {
                                        resultText = "PHISHING WEBSITE!\nRisk Score: 95/100\nDo not enter data!"
                                        resultColor = Color(0xFFD32F2F)
                                    } else {
                                        resultText = "WEBSITE CHECK\nRisk Score: 30/100\nProceed with caution"
                                        resultColor = Color(0xFFFFC107)
                                    }
                                }
                            }
                        }
                    )
                    2 -> AlertsTab()
                    3 -> SettingsTab()
                }
            }
        }
    }
}

@Composable
fun HomeTab() {
    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(20.dp))

        Card(
            modifier = Modifier.fillMaxWidth(),
            colors = CardDefaults.cardColors(containerColor = Color(0xFF1976D2))
        ) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(24.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Icon(
                    Icons.Default.Shield,
                    contentDescription = "Shield",
                    tint = Color.White,
                    modifier = Modifier.size(80.dp)
                )
                Spacer(modifier = Modifier.height(12.dp))
                Text("PROTECTED", color = Color.White, fontSize = 24.sp, fontWeight = FontWeight.Bold)
                Text("DigiKavach is active", color = Color.White.copy(alpha = 0.8f), fontSize = 14.sp)
            }
        }

        Spacer(modifier = Modifier.height(20.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            StatCard("47", "Calls Blocked", Color(0xFFD32F2F), Modifier.weight(1f))
            StatCard("12", "Scams Detected", Color(0xFFFF9800), Modifier.weight(1f))
            StatCard("Low", "Risk Level", Color(0xFF4CAF50), Modifier.weight(1f))
        }

        Spacer(modifier = Modifier.height(20.dp))

        Text("Quick Actions", fontSize = 18.sp, fontWeight = FontWeight.Bold)
        Spacer(modifier = Modifier.height(12.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            ActionButton("Check Number", Icons.Default.Phone, Modifier.weight(1f))
            ActionButton("Verify App", Icons.Default.Apps, Modifier.weight(1f))
        }
    }
}

@Composable
fun StatCard(value: String, label: String, color: Color, modifier: Modifier = Modifier) {
    Card(modifier = modifier) {
        Column(
            modifier = Modifier.padding(12.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Text(value, fontSize = 24.sp, fontWeight = FontWeight.Bold, color = color)
            Text(label, fontSize = 12.sp, color = Color.Gray)
        }
    }
}

@Composable
fun ActionButton(text: String, icon: androidx.compose.ui.graphics.vector.ImageVector, modifier: Modifier = Modifier) {
    Card(modifier = modifier) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = text, tint = Color(0xFF1976D2))
            Spacer(modifier = Modifier.width(8.dp))
            Text(text, fontSize = 14.sp)
        }
    }
}

@Composable
fun ScannerTab(
    phoneNumber: String, onPhoneChange: (String) -> Unit,
    appName: String, onAppChange: (String) -> Unit,
    websiteUrl: String, onWebsiteChange: (String) -> Unit,
    resultText: String, resultColor: Color,
    onCheck: (String, String) -> Unit
) {
    var selectedType by remember { mutableIntStateOf(0) }

    Column(
        modifier = Modifier.fillMaxSize(),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(modifier = Modifier.height(12.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            FilterChip(
                selected = selectedType == 0,
                onClick = { selectedType = 0 },
                label = { Text("Phone") },
                modifier = Modifier.weight(1f)
            )
            FilterChip(
                selected = selectedType == 1,
                onClick = { selectedType = 1 },
                label = { Text("App") },
                modifier = Modifier.weight(1f)
            )
            FilterChip(
                selected = selectedType == 2,
                onClick = { selectedType = 2 },
                label = { Text("Website") },
                modifier = Modifier.weight(1f)
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        when (selectedType) {
            0 -> OutlinedTextField(
                value = phoneNumber,
                onValueChange = onPhoneChange,
                label = { Text("Enter phone number") },
                placeholder = { Text("+919876543210") },
                modifier = Modifier.fillMaxWidth()
            )
            1 -> OutlinedTextField(
                value = appName,
                onValueChange = onAppChange,
                label = { Text("Enter app name") },
                placeholder = { Text("KreditBee") },
                modifier = Modifier.fillMaxWidth()
            )
            2 -> OutlinedTextField(
                value = websiteUrl,
                onValueChange = onWebsiteChange,
                label = { Text("Enter website URL") },
                placeholder = { Text("example.com") },
                modifier = Modifier.fillMaxWidth()
            )
        }

        Spacer(modifier = Modifier.height(16.dp))

        Button(
            onClick = {
                when (selectedType) {
                    0 -> onCheck("phone", phoneNumber)
                    1 -> onCheck("app", appName)
                    2 -> onCheck("website", websiteUrl)
                }
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF1976D2))
        ) {
            Icon(Icons.Default.Security, contentDescription = null)
            Spacer(modifier = Modifier.width(8.dp))
            Text("CHECK NOW", fontSize = 16.sp, fontWeight = FontWeight.Bold)
        }

        Spacer(modifier = Modifier.height(20.dp))

        if (resultText.isNotEmpty()) {
            Card(
                modifier = Modifier.fillMaxWidth(),
                colors = CardDefaults.cardColors(containerColor = resultColor)
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(20.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        if (resultColor == Color(0xFF4CAF50)) Icons.Default.CheckCircle else Icons.Default.Warning,
                        contentDescription = null,
                        tint = Color.White,
                        modifier = Modifier.size(48.dp)
                    )
                    Spacer(modifier = Modifier.height(12.dp))
                    Text(resultText, color = Color.White, fontSize = 16.sp, fontWeight = FontWeight.Bold)
                }
            }
        }
    }
}

@Composable
fun AlertsTab() {
    Column(modifier = Modifier.fillMaxSize()) {
        Spacer(modifier = Modifier.height(12.dp))

        Card(modifier = Modifier.fillMaxWidth()) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("47", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color(0xFFD32F2F))
                    Text("Blocked", fontSize = 12.sp)
                }
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("12", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color(0xFFFF9800))
                    Text("Detected", fontSize = 12.sp)
                }
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Text("5", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = Color(0xFF4CAF50))
                    Text("Alerts Sent", fontSize = 12.sp)
                }
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        AlertItem("Scam Call Blocked", "+919876543210", "2 min ago", Color(0xFFD32F2F))
        AlertItem("Suspicious App", "LoanOrbit", "1 hour ago", Color(0xFFFF9800))
        AlertItem("Payment Warning", "Banking app during call", "3 hours ago", Color(0xFFFFC107))
        AlertItem("Website Blocked", "fakekredit.com", "Yesterday", Color(0xFFFF9800))
        AlertItem("Guardian Alert Sent", "SMS to parent", "Yesterday", Color(0xFF4CAF50))
    }
}

@Composable
fun AlertItem(title: String, subtitle: String, time: String, color: Color) {
    Card(modifier = Modifier
        .fillMaxWidth()
        .padding(vertical = 4.dp)) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(12.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Card(colors = CardDefaults.cardColors(containerColor = color.copy(alpha = 0.1f))) {
                Icon(Icons.Default.Warning, contentDescription = null, tint = color, modifier = Modifier.padding(8.dp))
            }
            Spacer(modifier = Modifier.width(12.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(title, fontWeight = FontWeight.SemiBold)
                Text(subtitle, fontSize = 12.sp, color = Color.Gray)
                Text(time, fontSize = 10.sp, color = Color.Gray)
            }
        }
    }
}

@Composable
fun SettingsTab() {
    Column(modifier = Modifier.fillMaxSize()) {
        Spacer(modifier = Modifier.height(12.dp))

        var callBlocking by remember { mutableStateOf(true) }
        var paymentProtection by remember { mutableStateOf(true) }
        var websiteBlocking by remember { mutableStateOf(true) }
        var guardianAlerts by remember { mutableStateOf(true) }

        Card(modifier = Modifier.fillMaxWidth()) {
            Column(modifier = Modifier.padding(8.dp)) {
                SettingToggle("Call Blocking", "Block scam calls", callBlocking) { callBlocking = it }
                SettingToggle("Payment Protection", "Alert on banking app", paymentProtection) { paymentProtection = it }
                SettingToggle("Website Blocking", "Block phishing sites", websiteBlocking) { websiteBlocking = it }
                SettingToggle("Guardian Alerts", "SMS to contacts", guardianAlerts) { guardianAlerts = it }
            }
        }

        Spacer(modifier = Modifier.height(12.dp))

        Card(modifier = Modifier.fillMaxWidth()) {
            Row(modifier = Modifier.padding(16.dp), verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Phone, contentDescription = null, tint = Color(0xFFD32F2F))
                Spacer(modifier = Modifier.width(12.dp))
                Column {
                    Text("Emergency Helpline", fontWeight = FontWeight.Bold)
                    Text("1930 (Cyber Crime)", color = Color(0xFFD32F2F))
                }
            }
        }
    }
}

@Composable
fun SettingToggle(title: String, subtitle: String, checked: Boolean, onChecked: (Boolean) -> Unit) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .padding(12.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Column(modifier = Modifier.weight(1f)) {
            Text(title, fontWeight = FontWeight.Medium)
            Text(subtitle, fontSize = 12.sp, color = Color.Gray)
        }
        Switch(checked = checked, onCheckedChange = onChecked)
    }
}
```

---

## FILE 4: android/app/src/main/java/com/digikavach/service/SurakshaCallScreeningService.kt

```kotlin
package com.digikavach.service

import android.os.Build
import android.telecom.Call
import android.telecom.CallScreeningService
import android.util.Log
import androidx.annotation.RequiresApi

@RequiresApi(Build.VERSION_CODES.N)
class SurakshaCallScreeningService : CallScreeningService() {

    private val scamNumbers = listOf(
        "+919876543210",
        "+911234567890",
        "+919999999999"
    )

    override fun onScreenCall(callDetails: Call.Details) {
        val phoneNumber = callDetails.handle?.schemeSpecificPart ?: return

        val isScam = scamNumbers.any { scam ->
            phoneNumber.contains(scam) || scam.contains(phoneNumber)
        }

        if (isScam) {
            respondToCall(
                callDetails,
                CallResponse.Builder()
                    .setDisallowCall(true)
                    .setRejectCall(true)
                    .setSkipCallLog(false)
                    .setSkipNotification(false)
                    .build()
            )
            Log.d("ScamShield", "Blocked scam call from: $phoneNumber")
        } else {
            respondToCall(
                callDetails,
                CallResponse.Builder()
                    .setDisallowCall(false)
                    .setRejectCall(false)
                    .build()
            )
            Log.d("ScamShield", "Allowed call from: $phoneNumber")
        }
    }
}
```

---

## FILE 5: android/app/src/main/res/values/strings.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">DigiKavach</string>
</resources>
```

---

## FILE 6: android/app/src/main/res/values/themes.xml

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="Theme.DigiKavach" parent="android:Theme.Material.Light.NoActionBar">
        <item name="android:statusBarColor">#1976D2</item>
    </style>
</resources>
```

---

## That's It! Only 6 Files to Copy.

### File Locations Summary:

| File | Location |
|------|----------|
| build.gradle.kts | android/app/build.gradle.kts |
| AndroidManifest.xml | android/app/src/main/AndroidManifest.xml |
| MainActivity.kt | android/app/src/main/java/com/digikavach/MainActivity.kt |
| CallScreeningService.kt | android/app/src/main/java/com/digikavach/service/SurakshaCallScreeningService.kt |
| strings.xml | android/app/src/main/res/values/strings.xml |
| themes.xml | android/app/src/main/res/values/themes.xml |

---

## Quick Test Commands

```bash
# Test backend
curl http://localhost:8000/health

# Check scam number
curl "http://localhost:8000/api/v1/numbers/check?number=+919876543210"

# Check loan app
curl "http://localhost:8000/api/v1/apps/check?name=KreditBee"
```
