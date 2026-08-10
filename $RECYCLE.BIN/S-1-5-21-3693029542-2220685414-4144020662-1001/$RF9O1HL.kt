package com.aljozi.fleet.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import java.util.UUID

@Entity(tableName = "pending_sync_logs")
data class PendingSyncLogEntity(
    @PrimaryKey val id: String = UUID.randomUUID().toString(),
    val driverId: String,
    val vehiclePlate: String,
    val vehicleType: String, // TRUCK or CAR
    val logType: String,     // ODO, FUEL, MAINTENANCE, FAULT, COMPLAINT
    val payloadJson: String,  // تفاصيل العملية بصيغة JSON
    val timestamp: Long = System.currentTimeMillis(),
    val latitude: Double? = null,
    val longitude: Double? = null,
    val isSynced: Boolean = false
)