package com.surakshashield

import android.app.Application
import android.app.NotificationChannel
import android.app.NotificationManager
import android.os.Build
import com.surakshashield.data.database.AppDatabase
import com.surakshashield.data.repository.ScamRepository

class SurakshaShieldApp : Application() {

    val database by lazy { AppDatabase.getDatabase(this) }
    val repository by lazy { ScamRepository(database) }

    override fun onCreate() {
        super.onCreate()
        instance = this
        createNotificationChannels()
    }

    private fun createNotificationChannels() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            val scamAlertChannel = NotificationChannel(
                CHANNEL_SCAM_ALERT,
                "Scam Alerts",
                NotificationManager.IMPORTANCE_HIGH
            ).apply {
                description = "Alerts for scam calls and messages"
                enableVibration(true)
            }

            val guardianAlertChannel = NotificationChannel(
                CHANNEL_GUARDIAN_ALERT,
                "Guardian Notifications",
                NotificationManager.IMPORTANCE_DEFAULT
            ).apply {
                description = "Alerts sent to guardian contacts"
            }

            val protectionChannel = NotificationChannel(
                CHANNEL_PROTECTION,
                "Protection Status",
                NotificationManager.IMPORTANCE_LOW
            ).apply {
                description = "Protection service status"
            }

            val notificationManager = getSystemService(NotificationManager::class.java)
            notificationManager.createNotificationChannels(
                listOf(scamAlertChannel, guardianAlertChannel, protectionChannel)
            )
        }
    }

    companion object {
        const val CHANNEL_SCAM_ALERT = "scam_alert"
        const val CHANNEL_GUARDIAN_ALERT = "guardian_alert"
        const val CHANNEL_PROTECTION = "protection"

        lateinit var instance: SurakshaShieldApp
            private set
    }
}
