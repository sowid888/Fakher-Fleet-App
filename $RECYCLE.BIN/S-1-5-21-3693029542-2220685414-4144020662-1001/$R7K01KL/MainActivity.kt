package com.aljozi.fleet.ui.main

import android.content.Intent
import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.aljozi.fleet.databinding.ActivityMainBinding
import com.aljozi.fleet.ui.modules.FaultReportActivity
import com.aljozi.fleet.ui.modules.OdoFuelActivity

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        // فتح شاشة مسح العداد والوقود عبر الكاميرا والذكاء الاصطناعي
        binding.btnOpenScan.setOnClickListener {
            val intent = Intent(this, OdoFuelActivity::class.java)
            startActivity(intent)
        }

        // فتح شاشة تسجيل البلاغات والأعطال
        binding.btnOpenFault.setOnClickListener {
            val intent = Intent(this, FaultReportActivity::class.java)
            startActivity(intent)
        }

        // زر المزامنة اليدوية الفورية
        binding.btnForceSync.setOnClickListener {
            Toast.makeText(this, "جاري فحص البيانات غير المزامنة وإرسالها للسيرفر...", Toast.LENGTH_SHORT).show()
        }
    }
}