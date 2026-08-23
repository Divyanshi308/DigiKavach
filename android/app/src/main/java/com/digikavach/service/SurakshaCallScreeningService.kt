package com.digikavach.service

import android.content.Intent
import android.os.Build
import android.telecom.Call
import android.telecom.CallScreeningService
import android.util.Log
import androidx.annotation.RequiresApi
import com.digikavach.DigiKavachApp
import com.digikavach.data.repository.ScamRepository
import com.digikavach.ui.ScamAlertActivity
import kotlinx.coroutines.*

@RequiresApi(Build.VERSION_CODES.N)
class SurakshaCallScreeningService : CallScreeningService() {

    private val repository = DigiKavachApp.instance.repository
    private val scope = CoroutineScope(Dispatchers.IO + SupervisorJob())

    override fun onScreenCall(callDetails: Call.Details) {
        val direction = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            callDetails.callDirection
        } else {
            Call.Details.DIRECTION_INCOMING
        }

        // Only screen incoming calls
        if (direction == Call.Details.DIRECTION_INCOMING) {
            val phoneNumber = callDetails.handle?.schemeSpecificPart ?: return
            
            scope.launch {
                try {
                    // Check if number is a known scam number
                    val isScam = repository.isScamNumber(phoneNumber)
                    val riskScore = repository.getNumberRiskScore(phoneNumber)
                    
                    if (isScam || riskScore > 70) {
                        // Block the call and show alert
                        respondToCall(
                            callDetails,
                            CallResponse.Builder()
                                .setDisallowCall(true)
                                .setRejectCall(true)
                                .setSkipCallLog(false)
                                .setSkipNotification(false)
                                .build()
                        )
                        
                        // Show scam alert
                        showScamAlert(phoneNumber, riskScore, isScam)
                        
                        Log.d(TAG, "Blocked scam call from: $phoneNumber (Risk: $riskScore)")
                    } else {
                        // Allow the call
                        respondToCall(
                            callDetails,
                            CallResponse.Builder()
                                .setDisallowCall(false)
                                .setRejectCall(false)
                                .setSkipCallLog(false)
                                .setSkipNotification(false)
                                .build()
                        )
                        
                        Log.d(TAG, "Allowed call from: $phoneNumber (Risk: $riskScore)")
                    }
                } catch (e: Exception) {
                    Log.e(TAG, "Error screening call", e)
                    // Allow call on error
                    respondToCall(
                        callDetails,
                        CallResponse.Builder()
                            .setDisallowCall(false)
                            .build()
                    )
                }
            }
        } else {
            // Allow outgoing calls
            respondToCall(
                callDetails,
                CallResponse.Builder()
                    .setDisallowCall(false)
                    .build()
            )
        }
    }

    private fun showScamAlert(phoneNumber: String, riskScore: Int, isKnownScam: Boolean) {
        val intent = Intent(this, ScamAlertActivity::class.java).apply {
            addFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            addFlags(Intent.FLAG_ACTIVITY_SINGLE_TOP)
            putExtra("PHONE_NUMBER", phoneNumber)
            putExtra("RISK_SCORE", riskScore)
            putExtra("IS_KNOWN_SCAM", isKnownScam)
        }
        startActivity(intent)
    }

    override fun onDestroy() {
        super.onDestroy()
        scope.cancel()
    }

    companion object {
        private const val TAG = "CallScreeningService"
    }
}
