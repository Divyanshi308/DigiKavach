package com.surakshashield.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.surakshashield.ui.theme.*

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ScannerScreen() {
    var searchQuery by remember { mutableStateOf("") }
    var selectedTab by remember { mutableIntStateOf(0) }
    var isChecking by remember { mutableStateOf(false) }
    var result by remember { mutableStateOf<ScanResult?>(null) }

    val tabs = listOf("Phone Number", "Loan App", "Website", "QR Code")

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
            .padding(16.dp)
            .verticalScroll(rememberScrollState())
    ) {
        // Search Bar
        OutlinedTextField(
            value = searchQuery,
            onValueChange = { searchQuery = it },
            modifier = Modifier
                .fillMaxWidth()
                .padding(bottom = 16.dp),
            placeholder = { 
                Text(when (selectedTab) {
                    0 -> "Enter phone number (e.g., +919876543210)"
                    1 -> "Enter app name (e.g., KreditBee)"
                    2 -> "Enter website URL"
                    3 -> "Scan or paste UPI ID"
                    else -> "Enter to check..."
                })
            },
            leadingIcon = {
                Icon(Icons.Default.Search, contentDescription = "Search")
            },
            trailingIcon = {
                if (searchQuery.isNotEmpty()) {
                    IconButton(onClick = { searchQuery = ""; result = null }) {
                        Icon(Icons.Default.Clear, contentDescription = "Clear")
                    }
                }
            },
            keyboardOptions = KeyboardOptions(
                keyboardType = when (selectedTab) {
                    0 -> KeyboardType.Phone
                    2 -> KeyboardType.Uri
                    else -> KeyboardType.Text
                }
            ),
            shape = RoundedCornerShape(16.dp),
            singleLine = true
        )

        // Tabs
        TabRow(
            selectedTabIndex = selectedTab,
            modifier = Modifier.padding(bottom = 16.dp),
            containerColor = MaterialTheme.colorScheme.surface,
            contentColor = MaterialTheme.colorScheme.primary
        ) {
            tabs.forEachIndexed { index, title ->
                Tab(
                    selected = selectedTab == index,
                    onClick = { 
                        selectedTab = index
                        searchQuery = ""
                        result = null
                    },
                    text = { 
                        Text(
                            text = title,
                            fontSize = 12.sp
                        ) 
                    },
                    icon = {
                        Icon(
                            imageVector = when (index) {
                                0 -> Icons.Default.Phone
                                1 -> Icons.Default.Apps
                                2 -> Icons.Default.Language
                                3 -> Icons.Default.QrCodeScanner
                                else -> Icons.Default.Search
                            },
                            contentDescription = title,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                )
            }
        }

        // Check Button
        Button(
            onClick = {
                isChecking = true
                // Simulate checking
                result = ScanResult(
                    type = when (selectedTab) {
                        0 -> "Phone Number"
                        1 -> "Loan App"
                        2 -> "Website"
                        3 -> "UPI ID"
                        else -> "Unknown"
                    },
                    input = searchQuery,
                    isSafe = searchQuery.length > 5, // Mock check
                    riskScore = if (searchQuery.length > 5) 25 else 85,
                    riskLevel = if (searchQuery.length > 5) "safe" else "dangerous",
                    details = mapOf(
                        "source" to "Database check",
                        "last_updated" to "Just now"
                    )
                )
                isChecking = false
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(56.dp),
            enabled = searchQuery.isNotEmpty() && !isChecking,
            shape = RoundedCornerShape(16.dp)
        ) {
            if (isChecking) {
                CircularProgressIndicator(
                    modifier = Modifier.size(24.dp),
                    color = MaterialTheme.colorScheme.onPrimary
                )
            } else {
                Icon(Icons.Default.Security, contentDescription = null)
                Spacer(modifier = Modifier.width(8.dp))
                Text("CHECK NOW", fontSize = 16.sp, fontWeight = FontWeight.Bold)
            }
        }

        // Result Card
        result?.let { scanResult ->
            Spacer(modifier = Modifier.height(24.dp))
            
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(20.dp),
                colors = CardDefaults.cardColors(
                    containerColor = when (scanResult.riskLevel) {
                        "safe" -> RiskSafe
                        "suspicious" -> RiskSuspicious
                        "dangerous" -> RiskDangerous
                        "scam" -> RiskScam
                        else -> MaterialTheme.colorScheme.surface
                    }
                )
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    // Status Icon
                    Icon(
                        imageVector = if (scanResult.isSafe) 
                            Icons.Default.CheckCircle 
                        else 
                            Icons.Default.Warning,
                        contentDescription = null,
                        tint = Color.White,
                        modifier = Modifier.size(64.dp)
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Status Text
                    Text(
                        text = if (scanResult.isSafe) "SAFE" else "DANGER",
                        color = Color.White,
                        fontSize = 28.sp,
                        fontWeight = FontWeight.Bold
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // Type
                    Text(
                        text = scanResult.type,
                        color = Color.White.copy(alpha = 0.8f),
                        fontSize = 16.sp
                    )
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Risk Score
                    Card(
                        modifier = Modifier.fillMaxWidth(),
                        shape = RoundedCornerShape(12.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = Color.White.copy(alpha = 0.2f)
                        )
                    ) {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = "RISK SCORE",
                                color = Color.White.copy(alpha = 0.8f),
                                fontSize = 12.sp
                            )
                            Text(
                                text = "${scanResult.riskScore}/100",
                                color = Color.White,
                                fontSize = 32.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Details
                    scanResult.details.forEach { (key, value) ->
                        Row(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp),
                            horizontalArrangement = Arrangement.SpaceBetween
                        ) {
                            Text(
                                text = key.replace("_", " ").uppercase(),
                                color = Color.White.copy(alpha = 0.7f),
                                fontSize = 12.sp
                            )
                            Text(
                                text = value,
                                color = Color.White,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }
                    
                    Spacer(modifier = Modifier.height(16.dp))
                    
                    // Action Buttons
                    if (!scanResult.isSafe) {
                        Button(
                            onClick = { /* Report */ },
                            modifier = Modifier.fillMaxWidth(),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color.White
                            ),
                            shape = RoundedCornerShape(12.dp)
                        ) {
                            Icon(Icons.Default.Flag, contentDescription = null)
                            Spacer(modifier = Modifier.width(8.dp))
                            Text("REPORT SCAM", color = RiskScam)
                        }
                    }
                }
            }
        }

        // Placeholder if no result
        if (result == null) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .height(200.dp),
                contentAlignment = Alignment.Center
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Icon(
                        imageVector = Icons.Default.Security,
                        contentDescription = null,
                        tint = MaterialTheme.colorScheme.primary.copy(alpha = 0.3f),
                        modifier = Modifier.size(80.dp)
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "Enter a phone number, app name, or website to check",
                        color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f),
                        textAlign = androidx.compose.ui.text.style.TextAlign.Center
                    )
                }
            }
        }
    }
}

data class ScanResult(
    val type: String,
    val input: String,
    val isSafe: Boolean,
    val riskScore: Int,
    val riskLevel: String,
    val details: Map<String, String>
)
