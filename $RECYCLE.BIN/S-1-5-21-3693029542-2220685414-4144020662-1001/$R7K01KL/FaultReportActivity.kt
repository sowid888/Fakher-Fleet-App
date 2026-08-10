package com.aljozi.fleet.ui.modules

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.lifecycleScope
import com.aljozi.fleet.data.local.AppDatabase
import com.aljozi.fleet.data.local.entity.PendingSyncLogEntity
import com.aljozi.fleet.databinding.ActivityFaultReportBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class FaultReportActivity : AppCompatActivity() {

    private lateinit var binding: ActivityFaultReportBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityFaultReportBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnAttachPhoto.setOnClickListener {
            Toast.makeText(this, "سيتم فتح الكاميرا لالتقاط صورة العطل", Toast.LENGTH_SHORT).show()
        }

        binding.btnSubmitReport.setOnClickListener {
            val type = binding.etReportType.text.toString().trim()
            val desc = binding.etDescription.text.toString().trim()

            if (type.isEmpty() || desc.isEmpty()) {
                Toast.makeText(this, "يرجى تعبئة كافة الحقول المطلوب", Toast.LENGTH_SHORT).show()
                return@setOnClickListener
            }

            saveReportLocally(type, desc)
        }
    }

    private fun saveReportLocally(type: String, description: String) {
        lifecycleScope.launch(Dispatchers.IO) {
            val db = AppDatabase.getDatabase(applicationContext, "SecurePassphrase123!".toByteArray())
            val log = PendingSyncLogEntity(
                driverId = "DRV_CURRENT",
                vehiclePlate = "1234-A",
                vehicleType = "TRUCK",
                logType = "FAULT",
                payloadJson = "{\"type\":\"$type\", \"desc\":\"$description\"}"
            )
            db.pendingSyncLogDao().insertLog(log)

            withContext(Dispatchers.Main) {
                Toast.makeText(this@FaultReportActivity, "تم تسجيل البلاغ بنجاح وحفظه للمزامنة", Toast.LENGTH_LONG).show()
                finish()
            }
        }
    }
}