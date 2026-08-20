package com.surakshashield.data.repository

import com.surakshashield.data.*
import com.surakshashield.data.database.AppDatabase
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class ScamRepository(private val database: AppDatabase) {

    // Mock scam numbers database (in production, sync from backend)
    private val scamNumbersDb = mutableMapOf(
        "+919876543210" to ScamNumber(
            phoneNumber = "+919876543210",
            riskScore = 95,
            riskLevel = "scam",
            source = "DoT MNRL",
            reports = 1250,
            type = "digital_arrest_scam",
            isActive = true,
            lastUpdated = System.currentTimeMillis()
        ),
        "+911234567890" to ScamNumber(
            phoneNumber = "+911234567890",
            riskScore = 88,
            riskLevel = "dangerous",
            source = "I4C Registry",
            reports = 890,
            type = "loan_fraud",
            isActive = true,
            lastUpdated = System.currentTimeMillis()
        ),
        "+919999999999" to ScamNumber(
            phoneNumber = "+919999999999",
            riskScore = 15,
            riskLevel = "safe",
            source = "Verified",
            reports = 0,
            type = null,
            isActive = false,
            lastUpdated = System.currentTimeMillis()
        )
    )

    // Mock loan apps database
    private val loanAppsDb = mutableMapOf(
        "kreditbee" to LoanApp(
            appName = "KreditBee",
            isLegitimate = true,
            riskScore = 15,
            riskLevel = "safe",
            nbfcName = "KreditBee Finance India Private Limited",
            nbfcRegistration = "NBFC-HC-Company-2018-1286",
            appStoreUrl = "https://play.google.com/store/apps/details?id=com.kreditbee",
            website = "https://www.kreditbee.in",
            lastUpdated = System.currentTimeMillis()
        ),
        "loanorbit" to LoanApp(
            appName = "LoanOrbit",
            isLegitimate = false,
            riskScore = 95,
            riskLevel = "dangerous",
            nbfcName = null,
            nbfcRegistration = null,
            appStoreUrl = null,
            website = null,
            lastUpdated = System.currentTimeMillis()
        )
    )

    // Check if a number is a known scam number
    suspend fun isScamNumber(phoneNumber: String): Boolean = withContext(Dispatchers.IO) {
        val normalized = normalizeNumber(phoneNumber)
        
        // Check local database first
        if (scamNumbersDb.containsKey(normalized)) {
            return@withContext scamNumbersDb[normalized]?.isActive == true &&
                   scamNumbersDb[normalized]?.riskScore!! > 70
        }
        
        // Check Room database
        val dbNumber = database.scamNumberDao().getScamNumber(normalized)
        if (dbNumber != null) {
            return@withContext dbNumber.isActive && dbNumber.riskScore > 70
        }
        
        false
    }

    // Get risk score for a number (0-100)
    suspend fun getNumberRiskScore(phoneNumber: String): Int = withContext(Dispatchers.IO) {
        val normalized = normalizeNumber(phoneNumber)
        
        // Check local database
        scamNumbersDb[normalized]?.let { return@withContext it.riskScore }
        
        // Check Room database
        database.scamNumberDao().getScamNumber(normalized)?.let { return@withContext it.riskScore }
        
        // Default risk score for unknown numbers
        10
    }

    // Check if a loan app is legitimate
    suspend fun isLegitimateLoanApp(appName: String): Boolean = withContext(Dispatchers.IO) {
        val normalized = appName.lowercase().replace(" ", "")
        
        // Check local database
        loanAppsDb[normalized]?.let { return@withContext it.isLegitimate }
        
        // Check Room database
        database.loanAppDao().getLoanApp(normalized)?.let { return@withContext it.isLegitimate }
        
        // Not found - assume suspicious
        false
    }

    // Get loan app details
    suspend fun getLoanAppDetails(appName: String): LoanApp? = withContext(Dispatchers.IO) {
        val normalized = appName.lowercase().replace(" ", "")
        
        // Check local database
        loanAppsDb[normalized]?.let { return@withContext it }
        
        // Check Room database
        database.loanAppDao().getLoanApp(normalized)
    }

    // Report a scam number
    suspend fun reportScamNumber(phoneNumber: String, reportType: String, description: String?) = withContext(Dispatchers.IO) {
        val normalized = normalizeNumber(phoneNumber)
        
        // Update or create entry
        val existing = scamNumbersDb[normalized]
        if (existing != null) {
            scamNumbersDb[normalized] = existing.copy(
                reports = existing.reports + 1,
                lastUpdated = System.currentTimeMillis()
            )
        } else {
            scamNumbersDb[normalized] = ScamNumber(
                phoneNumber = normalized,
                riskScore = 60, // Start with medium risk
                riskLevel = "suspicious",
                source = "community",
                reports = 1,
                type = reportType,
                isActive = true,
                lastUpdated = System.currentTimeMillis()
            )
        }
        
        // Save to Room database
        scamNumbersDb[normalized]?.let {
            database.scamNumberDao().insertScamNumber(it)
        }
    }

    // Get all blocked numbers
    suspend fun getBlockedNumbers(): List<ScamNumber> = withContext(Dispatchers.IO) {
        scamNumbersDb.values.filter { it.isActive && it.riskScore > 70 }
    }

    // Get all legitimate loan apps
    suspend fun getLegitimateLoanApps(): List<LoanApp> = withContext(Dispatchers.IO) {
        loanAppsDb.values.filter { it.isLegitimate }
    }

    // Get all blocked loan apps
    suspend fun getBlockedLoanApps(): List<LoanApp> = withContext(Dispatchers.IO) {
        loanAppsDb.values.filter { !it.isLegitimate }
    }

    // Normalize phone number
    private fun normalizeNumber(number: String): String {
        val cleaned = number.trim().replace(" ", "").replace("-", "")
        return when {
            cleaned.startsWith("+91") -> cleaned
            cleaned.startsWith("91") && cleaned.length == 12 -> "+$cleaned"
            cleaned.length == 10 -> "+91$cleaned"
            else -> cleaned
        }
    }
}
