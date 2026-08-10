package com.aljozi.fleet.data.remote

import android.content.Context
import androidx.work.CoroutineWorker
import androidx.work.WorkerParameters
import com.aljozi.fleet.data.local.AppDatabase
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

class SyncWorker(
    appContext: Context,
    workerParams: WorkerParameters
) : CoroutineWorker(appContext, workerParams) {

    override suspend fun doWork(): Result = withContext(Dispatchers.IO) {
        try {
            val db = AppDatabase.getDatabase(applicationContext, "SecurePassphrase123!".toByteArray())
            val pendingLogs = db.pendingSyncLogDao().getUnsyncedLogs()

            if (pendingLogs.isNotEmpty()) {
                // محاكاة رفع البيانات غير المزامنة إلى السيرفر الرئيسي
                for (log in pendingLogs) {
                    // بعد تمام الرفع بنجاح للسيرفر يتم تحديث الحالة في قاعدة البيانات المحلية
                    db.pendingSyncLogDao().markAsSynced(log.id)
                }
            }

            Result.success()
        } catch (e: Exception) {
            Result.retry()
        }
    }
}