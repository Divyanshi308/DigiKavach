package com.digikavach.receiver

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.os.Build
import android.util.Log
import com.digikavach.service.PaymentProtectionService

class BootReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        if (intent.action == Intent.ACTION_BOOT_COMPLETED) {
            Log.d(TAG, "Device booted, starting DigiKavach services")
            
            // Start payment protection service
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                context.startForegroundService(
                    Intent(context, PaymentProtectionService::class.java).apply {
                        action = PaymentProtectionService.ACTION_START_MONITORING
                    }
                )
            } else {
                context.startService(
                    Intent(context, PaymentProtectionService::class.java).apply {
                        action = PaymentProtectionService.ACTION_START_MONITORING
                    }
                )
            }
        }
    }

    companion object {
        private const val TAG = "BootReceiver"
    }
}
