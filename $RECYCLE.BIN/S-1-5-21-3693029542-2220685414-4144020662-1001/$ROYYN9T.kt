package com.aljozi.fleet.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import com.aljozi.fleet.data.local.entity.PendingSyncLogEntity

@Dao
interface PendingSyncLogDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertLog(log: PendingSyncLogEntity)

    @Query("SELECT * FROM pending_sync_logs WHERE isSynced = 0 ORDER BY timestamp ASC")
    suspend fun getUnsyncedLogs(): List<PendingSyncLogEntity>

    @Query("UPDATE pending_sync_logs SET isSynced = 1 WHERE id = :logId")
    suspend fun markAsSynced(logId: String)

    @Query("DELETE FROM pending_sync_logs WHERE isSynced = 1")
    suspend fun clearSyncedLogs()
}