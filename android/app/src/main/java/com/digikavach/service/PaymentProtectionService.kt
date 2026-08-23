package com.digikavach.service

import android.app.*
import android.content.Context
import android.content.Intent
import android.os.Build
import android.os.IBinder
import android.util.Log
import androidx.core.app.NotificationCompat
import com.digikavach.R
import com.digikavach.DigiKavachApp
import com.digikavach.data.repository.ScamRepository
import com.digikavach.ui.ScamAlertActivity
import kotlinx.coroutines.*

class PaymentProtectionService : Service() {

    private val repository = DigiKavachApp.instance.repository
    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())
    
    private var isMonitoring = false
    private var currentCallNumber: String? = null
    private var isOnCall = false

    override fun onBind(intent: Intent?): IBinder? = null

    override fun onCreate() {
        super.onCreate()
        startForegroundService()
    }

    override fun onStartCommand(intent: Intent?, flags: Int, startId: Int): Int {
        when (intent?.action) {
            ACTION_START_MONITORING -> startMonitoring()
            ACTION_STOP_MONITORING -> stopMonitoring()
            ACTION_CALL_STARTED -> {
                currentCallNumber = intent.getStringExtra(EXTRA_PHONE_NUMBER)
                isOnCall = true
            }
            ACTION_CALL_ENDED -> {
                isOnCall = false
                currentCallNumber = null
            }
            ACTION_APP_OPENED -> {
                val packageName = intent.getStringExtra(EXTRA_PACKAGE_NAME)
                checkForSuspiciousActivity(packageName)
            }
        }
        return START_STICKY
    }

    private fun startMonitoring() {
        if (isMonitoring) return
        isMonitoring = true
        Log.d(TAG, "Payment protection monitoring started")
    }

    private fun stopMonitoring() {
        isMonitoring = false
        Log.d(TAG, "Payment protection monitoring stopped")
    }

    private fun checkForSuspiciousActivity(packageName: String?) {
        if (!isOnCall || packageName == null) return
        
        // Check if user opened banking/UPI app during an unknown call
        val bankingApps = listOf(
            "com.google.android.apps.nbu.paisa.user", // Google Pay
            "com.phonepe.app", // PhonePe
            "net.one97.paytm", // Paytm
            "com.bhim.axis", // BHIM
            "com.csam.icici.bank.imobile", // ICICI
            "com.hdfcbank.hdfcbank", // HDFC
            "com.sbi.SBAmong", // SBI
            "com.axis.mobile", // Axis
            "in.amazon.mShop.android.shopping" // Amazon Pay
        )
        
        if (packageName in bankingApps) {
            // Check if current call is from unknown/suspicious number
            currentCallNumber?.let { number ->
                scope.launch {
                    val isSuspicious = repository.isScamNumber(number) || 
                                      repository.getNumberRiskScore(number) > 50
                    
                    if (isSuspicious) {
                        showPaymentWarning(number, packageName)
                    }
                }
            }
        }
    }

    private fun showPaymentWarning(phoneNumber: String, packageName: String) {
        val intent = Intent(this, ScamAlertActivity::class.java).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
            putExtra("ALERT_TYPE", "PAYMENT_WARNING")
            putExtra("PHONE_NUMBER", phoneNumber)
            putExtra("PACKAGE_NAME", packageName)
            putExtra("MESSAGE", "WARNING: You're on a call with a suspicious number and opened a banking app!")
        }
        startActivity(intent)
        
        // Send notification
        sendPaymentWarningNotification(phoneNumber)
    }

    private fun sendPaymentWarningNotification(phoneNumber: String) {
        val intent = Intent(this, ScamAlertActivity::class.java).apply {
            putExtra("PHONE_NUMBER", phoneNumber)
        }
        val pendingIntent = PendingIntent.getActivity(
            this, 0, intent,
            PendingIntent.FLAG_UPDATE_CURRENT or PendingIntent.FLAG_IMMUTABLE
        )

        val notification = NotificationCompat.Builder(this, DigiKavachApp.CHANNEL_SCAM_ALERT)
            .setSmallIcon(R.drawable.ic_shield)
            .setContentTitle("⚠️ Payment Warning!")
            .setContentText("Suspicious call detected while banking app is open")
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setContentIntent(pendingIntent)
            .setAutoCancel(true)
            .build()

        val notificationManager = getSystemService(Context.NOTIFICATION_SERVICE) as NotificationManager
        notificationManager.notify(NOTIFICATION_PAYMENT_WARNING, notification)
    }

    private fun startForegroundService() {
        val notification = NotificationCompat.Builder(this, DigiKavachApp.CHANNEL_PROTECTION)
            .setSmallIcon(R.drawable.ic_shield)
            .setContentTitle("DigiKavach Active")
            .setContentText("Protecting you from fraud")
            .setPriority(NotificationCompat.PRIORITY_LOW)
            .setOngoing(true)
            .build()

        startForeground(NOTIFICATION_ID, notification)
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }

    companion object {
        private const val TAG = "PaymentProtection"
        private const val NOTIFICATION_ID = 1001
        private const val NOTIFICATION_PAYMENT_WARNING = 1002

        const val ACTION_START_MONITORING = "com.digikavach.START_MONITORING"
        const val ACTION_STOP_MONITORING = "com.digikavach.STOP_MONITORING"
        const val ACTION_CALL_STARTED = "com.digikavach.CALL_STARTED"
        const val ACTION_CALL_ENDED = "com.digikavach.CALL_ENDED"
        const val ACTION_APP_OPENED = "com.digikavach.APP_OPENED"
        
        const val EXTRA_PHONE_NUMBER = "phone_number"
        const val EXTRA_PACKAGE_NAME = "package_name"

        fun startService(context: Context) {
            val intent = Intent(context, PaymentProtectionService::class.java).apply {
                action = ACTION_START_MONITORING
            }
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(intent)
            } else {
                context.startService(intent)
            }
        }

        fun stopService(context: Context) {
            val intent = Intent(context, PaymentProtectionService::class.java).apply {
                action = ACTION_STOP_MONITORING
            }
            context.stopService(intent)
        }
    }
}
