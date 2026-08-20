package com.surakshashield.ui

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Warning
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.surakshashield.ui.theme.SurakshaShieldTheme
import kotlinx.coroutines.delay

class ScamAlertActivity : ComponentActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        
        val phoneNumber = intent.getStringExtra("PHONE_NUMBER") ?: "Unknown"
        val riskScore = intent.getIntExtra("RISK_SCORE", 0)
        val isKnownScam = intent.getBooleanExtra("IS_KNOWN_SCAM", false)
        val alertType = intent.getStringExtra("ALERT_TYPE") ?: "SCAM_CALL"
        val message = intent.getStringExtra("MESSAGE") ?: "This number is flagged as suspicious!"

        setContent {
            SurakshaShieldTheme {
                ScamAlertScreen(
                    phoneNumber = phoneNumber,
                    riskScore = riskScore,
                    isKnownScam = isKnownScam,
                    alertType = alertType,
                    message = message,
                    onDismiss = { finish() },
                    onBlock = { 
                        // Block the number
                        finish()
                    },
                    onReport = { 
                        // Report the number
                        finish()
                    }
                )
            }
        }
    }
}

@Composable
fun ScamAlertScreen(
    phoneNumber: String,
    riskScore: Int,
    isKnownScam: Boolean,
    alertType: String,
    message: String,
    onDismiss: () -> Unit,
    onBlock: () -> Unit,
    onReport: () -> Unit
) {
    var countdown by remember { mutableIntStateOf(10) }
    
    LaunchedEffect(Unit) {
        while (countdown > 0) {
            delay(1000)
            countdown--
        }
    }

    val backgroundColor = when {
        riskScore > 80 -> Color(0xFFD32F2F) // Red
        riskScore > 60 -> Color(0xFFFF6F00) // Orange
        riskScore > 40 -> Color(0xFFFFC107) // Yellow
        else -> Color(0xFF4CAF50) // Green
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(backgroundColor)
            .padding(24.dp),
        contentAlignment = Alignment.Center
    ) {
        Column(
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center,
            modifier = Modifier.fillMaxSize()
        ) {
            // Warning Icon
            Icon(
                imageVector = Icons.Default.Warning,
                contentDescription = "Warning",
                tint = Color.White,
                modifier = Modifier.size(120.dp)
            )
            
            Spacer(modifier = Modifier.height(24.dp))
            
            // Alert Title
            Text(
                text = if (isKnownScam) "SCAM CALL BLOCKED!" else "SUSPICIOUS CALL!",
                color = Color.White,
                fontSize = 28.sp,
                fontWeight = FontWeight.Bold,
                textAlign = TextAlign.Center
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Phone Number
            Text(
                text = phoneNumber,
                color = Color.White,
                fontSize = 24.sp,
                fontWeight = FontWeight.Medium
            )
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Risk Score
            Card(
                modifier = Modifier.padding(8.dp),
                shape = RoundedCornerShape(12.dp),
                colors = CardDefaults.cardColors(
                    containerColor = Color.White.copy(alpha = 0.2f)
                )
            ) {
                Column(
                    modifier = Modifier.padding(16.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(
                        text = "RISK SCORE",
                        color = Color.White.copy(alpha = 0.8f),
                        fontSize = 14.sp
                    )
                    Text(
                        text = "$riskScore/100",
                        color = Color.White,
                        fontSize = 36.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
            }
            
            Spacer(modifier = Modifier.height(16.dp))
            
            // Message
            Text(
                text = message,
                color = Color.White,
                fontSize = 16.sp,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(horizontal = 32.dp)
            )
            
            Spacer(modifier = Modifier.height(32.dp))
            
            // Buttons
            Column(
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.spacedBy(12.dp)
            ) {
                // Block Button
                Button(
                    onClick = onBlock,
                    modifier = Modifier
                        .fillMaxWidth(0.8f)
                        .height(56.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Color.White
                    ),
                    shape = RoundedCornerShape(28.dp)
                ) {
                    Text(
                        text = "BLOCK THIS NUMBER",
                        color = backgroundColor,
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                // Report Button
                OutlinedButton(
                    onClick = onReport,
                    modifier = Modifier
                        .fillMaxWidth(0.8f)
                        .height(56.dp),
                    colors = ButtonDefaults.outlinedButtonColors(
                        contentColor = Color.White
                    ),
                    shape = RoundedCornerShape(28.dp)
                ) {
                    Text(
                        text = "REPORT AS SCAM",
                        fontSize = 16.sp,
                        fontWeight = FontWeight.Medium
                    )
                }
                
                // Dismiss Button (with countdown)
                TextButton(
                    onClick = onDismiss,
                    enabled = countdown == 0,
                    modifier = Modifier.padding(top = 16.dp)
                ) {
                    Text(
                        text = if (countdown > 0) "Dismiss in ${countdown}s" else "Dismiss",
                        color = Color.White.copy(alpha = if (countdown > 0) 0.6f else 1f),
                        fontSize = 14.sp
                    )
                }
            }
        }
    }
}
