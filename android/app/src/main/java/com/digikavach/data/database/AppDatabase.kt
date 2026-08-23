package com.digikavach.data.database

import android.content.Context
import androidx.room.*
import com.digikavach.data.*

@Database(
    entities = [
        ScamNumber::class,
        LoanApp::class,
        BlockedWebsite::class,
        GuardianContact::class,
        CallLogEntry::class,
        AlertEntry::class
    ],
    version = 1,
    exportSchema = false
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun scamNumberDao(): ScamNumberDao
    abstract fun loanAppDao(): LoanAppDao
    abstract fun guardianDao(): GuardianDao
    abstract fun callLogDao(): CallLogDao
    abstract fun alertDao(): AlertDao

    companion object {
        @Volatile
        private var INSTANCE: AppDatabase? = null

        fun getDatabase(context: Context): AppDatabase {
            return INSTANCE ?: synchronized(this) {
                val instance = Room.databaseBuilder(
                    context.applicationContext,
                    AppDatabase::class.java,
                    "surakshashield_database"
                )
                .fallbackToDestructiveMigration()
                .build()
                INSTANCE = instance
                instance
            }
        }
    }
}

@Dao
interface ScamNumberDao {
    @Query("SELECT * FROM scam_numbers WHERE phoneNumber = :number")
    suspend fun getScamNumber(number: String): ScamNumber?

    @Query("SELECT * FROM scam_numbers WHERE isActive = 1")
    suspend fun getAllActiveScamNumbers(): List<ScamNumber>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertScamNumber(scamNumber: ScamNumber)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(scamNumbers: List<ScamNumber>)

    @Query("UPDATE scam_numbers SET riskScore = :score WHERE phoneNumber = :number")
    suspend fun updateRiskScore(number: String, score: Int)

    @Query("DELETE FROM scam_numbers WHERE phoneNumber = :number")
    suspend fun deleteScamNumber(number: String)
}

@Dao
interface LoanAppDao {
    @Query("SELECT * FROM loan_apps WHERE appName = :name")
    suspend fun getLoanApp(name: String): LoanApp?

    @Query("SELECT * FROM loan_apps WHERE isLegitimate = 1")
    suspend fun getAllLegitimateApps(): List<LoanApp>

    @Query("SELECT * FROM loan_apps WHERE isLegitimate = 0")
    suspend fun getAllBlockedApps(): List<LoanApp>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLoanApp(loanApp: LoanApp)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(loanApps: List<LoanApp>)
}

@Dao
interface GuardianDao {
    @Query("SELECT * FROM guardian_contacts WHERE userId = :userId")
    suspend fun getGuardian(userId: String): GuardianContact?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertGuardian(guardian: GuardianContact)

    @Delete
    suspend fun deleteGuardian(guardian: GuardianContact)
}

@Dao
interface CallLogDao {
    @Query("SELECT * FROM call_logs ORDER BY timestamp DESC LIMIT :limit")
    suspend fun getRecentCalls(limit: Int = 50): List<CallLogEntry>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertCallLog(callLog: CallLogEntry)

    @Query("SELECT COUNT(*) FROM call_logs WHERE wasBlocked = 1")
    suspend fun getBlockedCallsCount(): Int
}

@Dao
interface AlertDao {
    @Query("SELECT * FROM alert_history WHERE userId = :userId ORDER BY timestamp DESC LIMIT :limit")
    suspend fun getAlerts(userId: String, limit: Int = 50): List<AlertEntry>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAlert(alert: AlertEntry)

    @Query("DELETE FROM alert_history WHERE userId = :userId")
    suspend fun clearAlerts(userId: String)
}
