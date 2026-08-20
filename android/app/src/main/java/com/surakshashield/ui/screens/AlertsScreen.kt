package com.surakshashield.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.surakshashield.ui.theme.*

@Composable
fun AlertsScreen() {
    var selectedTab by remember { mutableIntStateOf(0) }
    
    // Mock alert data
    val alerts = listOf(
        AlertItem(
            id = "1",
            type = "Scam Call Blocked",
            description = "Blocked call from +919876543210 (Digital Arrest Scam)",
            timestamp = "2 min ago",
            riskScore = 95,
            icon = Icons.Default.Phone,
            color = RiskScam
        ),
        AlertItem(
            id = "2",
            type = "Suspicious App Detected",
            description = "LoanOrbit app flagged as fraudulent",
            timestamp = "1 hour ago",
            riskScore = 92,
            icon = Icons.Default.Warning,
            color = RiskDangerous
        ),
        AlertItem(
            id = "3",
            type = "Payment Warning",
            description = "Attempted to open banking app during unknown call",
            timestamp = "3 hours ago",
            riskScore = 75,
            icon = Icons.Default.Payment,
            color = RiskSuspicious
        ),
        AlertItem(
            id = "4",
            type = "Website Blocked",
            description = "Blocked access to fakekredit.com (Phishing)",
            timestamp = "Yesterday",
            riskScore = 88,
            icon = Icons.Default.Language,
            color = RiskDangerous
        ),
        AlertItem(
            id = "5",
            type = "Guardian Alert Sent",
            description = "SMS sent to parent about suspicious activity",
            timestamp = "Yesterday",
            riskScore = 70,
            icon = Icons.Default.People,
            color = RiskSuspicious
        )
    )

    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(MaterialTheme.colorScheme.background)
    ) {
        // Tabs
        TabRow(
            selectedTabIndex = selectedTab,
            containerColor = MaterialTheme.colorScheme.surface,
            contentColor = MaterialTheme.colorScheme.primary
        ) {
            Tab(
                selected = selectedTab == 0,
                onClick = { selectedTab = 0 },
                text = { Text("Recent") },
                icon = { Icon(Icons.Default.AccessTime, contentDescription = null) }
            )
            Tab(
                selected = selectedTab == 1,
                onClick = { selectedTab = 1 },
                text = { Text("Blocked") },
                icon = { Icon(Icons.Default.Block, contentDescription = null) }
            )
            Tab(
                selected = selectedTab == 2,
                onClick = { selectedTab = 2 },
                text = { Text("Reports") },
                icon = { Icon(Icons.Default.Assessment, contentDescription = null) }
            )
        }

        // Stats Summary
        Card(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            shape = RoundedCornerShape(16.dp)
        ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(16.dp),
                horizontalArrangement = Arrangement.SpaceEvenly
            ) {
                StatItem(
                    value = "47",
                    label = "Calls Blocked",
                    color = RiskScam
                )
                StatItem(
                    value = "12",
                    label = "Scams Detected",
                    color = RiskDangerous
                )
                StatItem(
                    value = "5",
                    label = "Alerts Sent",
                    color = RiskSuspicious
                )
            }
        }

        // Alert List
        LazyColumn(
            modifier = Modifier
                .fillMaxSize()
                .padding(horizontal = 16.dp),
            verticalArrangement = Arrangement.spacedBy(12.dp)
        ) {
            items(alerts) { alert ->
                AlertCard(alert = alert)
            }
        }
    }
}

@Composable
fun StatItem(
    value: String,
    label: String,
    color: Color
) {
    Column(
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = value,
            fontSize = 24.sp,
            fontWeight = FontWeight.Bold,
            color = color
        )
        Text(
            text = label,
            fontSize = 12.sp,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
        )
    }
}

@Composable
fun AlertCard(alert: AlertItem) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(12.dp)
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            // Icon
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(alert.color.copy(alpha = 0.1f)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    imageVector = alert.icon,
                    contentDescription = null,
                    tint = alert.color,
                    modifier = Modifier.size(24.dp)
                )
            }
            
            Spacer(modifier = Modifier.width(12.dp))
            
            // Content
            Column(
                modifier = Modifier.weight(1f)
            ) {
                Text(
                    text = alert.type,
                    style = MaterialTheme.typography.titleSmall,
                    fontWeight = FontWeight.SemiBold
                )
                Text(
                    text = alert.description,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
                )
                Text(
                    text = alert.timestamp,
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.4f)
                )
            }
            
            // Risk Score Badge
            Box(
                modifier = Modifier
                    .clip(RoundedCornerShape(8.dp))
                    .background(alert.color.copy(alpha = 0.1f))
                    .padding(horizontal = 8.dp, vertical = 4.dp)
            ) {
                Text(
                    text = "${alert.riskScore}",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    color = alert.color
                )
            }
        }
    }
}

data class AlertItem(
    val id: String,
    val type: String,
    val description: String,
    val timestamp: String,
    val riskScore: Int,
    val icon: ImageVector,
    val color: Color
)
