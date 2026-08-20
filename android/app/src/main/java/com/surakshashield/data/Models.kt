package com.surakshashield.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "scam_numbers")
data class ScamNumber(
    @PrimaryKey
    val phoneNumber: String,
    val riskScore: Int,
    val riskLevel: String, // safe, suspicious, dangerous, scam
    val source: String, // DoT MNRL, I4C, RBI, community
    val reports: Int,
    val type: String?, // digital_arrest, loan_fraud, phishing, etc.
    val isActive: Boolean,
    val lastUpdated: Long
)

@Entity(tableName = "loan_apps")
data class LoanApp(
    @PrimaryKey
    val appName: String,
    val isLegitimate: Boolean,
    val riskScore: Int,
    val riskLevel: String,
    val nbfcName: String?,
    val nbfcRegistration: String?,
    val appStoreUrl: String?,
    val website: String?,
    val lastUpdated: Long
)

@Entity(tableName = "blocked_websites")
data class BlockedWebsite(
    @PrimaryKey
    val url: String,
    val isSafe: Boolean,
    val riskScore: Int,
    val riskLevel: String,
    val category: String?,
    val lastUpdated: Long
)

@Entity(tableName = "guardian_contacts")
data class GuardianContact(
    @PrimaryKey
    val userId: String,
    val name: String,
    val phone: String,
    val relationship: String,
    val createdAt: Long
)

@Entity(tableName = "call_logs")
data class CallLogEntry(
    @PrimaryKey
    val id: String,
    val phoneNumber: String,
    val timestamp: Long,
    val wasBlocked: Boolean,
    val riskScore: Int,
    val duration: Long
)

@Entity(tableName = "alert_history")
data class AlertEntry(
    @PrimaryKey
    val id: String,
    val userId: String,
    val alertType: String,
    val message: String,
    val timestamp: Long,
    val status: String
)
