/**
 * نظام الجوزي لإدارة الأسطول - إدارة قاعدة البيانات المحلية والمزامنة
 * بديل قاعدة البيانات المشفرة (AppDatabase / PendingSyncLogDao)
 */

const AppDatabase = {
    dbName: "aljozi_fleet_secure_db",
    dbVersion: 1,
    dbInstance: null,

    // تهيئة قاعدة البيانات المحلية عند تشغيل التطبيق
    initDatabase: function() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.dbVersion);

            request.onupgradeneeded = function(event) {
                const db = event.target.result;
                // إنشاء جدول سجلات المزامنة المعلقة (PendingSyncLogs)
                if (!db.objectStoreNames.contains("pendingSyncLogs")) {
                    const store = db.createObjectStore("pendingSyncLogs", { keyPath: "id", autoIncrement: true });
                    store.createIndex("timestamp", "timestamp", { unique: false });
                    store.createIndex("status", "status", { unique: false });
                }
            };

            request.onsuccess = (event) => {
                this.dbInstance = event.target.result;
                console.log("تمت تهيئة قاعدة البيانات المحلية بنجاح.");
                resolve(this.dbInstance);
            };

            request.onerror = (event) => {
                console.error("خطأ في فتح قاعدة البيانات المحلية:", event.target.error);
                reject(event.target.error);
            };
        });
    },

    // إضافة سجل جديد بانتظار المزامنة (مثل البلاغات أو مسح العداد)
    addPendingLog: function(logData) {
        return new Promise((resolve, reject) => {
            if (!this.dbInstance) {
                reject("قاعدة البيانات غير مهيأة بعد.");
                return;
            }
            const transaction = this.dbInstance.transaction(["pendingSyncLogs"], "readwrite");
            const store = transaction.objectStore("pendingSyncLogs");
            
            const logEntity = {
                payload: logData,
                timestamp: new Date().toISOString(),
                status: "PENDING"
            };

            const request = store.add(logEntity);

            request.onsuccess = () => {
                resolve({ success: true, message: "تم حفظ السجل محلياً بنجاح." });
            };

            request.onerror = (event) => {
                reject(event.target.error);
            };
        });
    },

    // جلب جميع السجلات المعلقة للمزامنة مع الخادم
    getPendingLogs: function() {
        return new Promise((resolve, reject) => {
            if (!this.dbInstance) {
                reject("قاعدة البيانات غير مهيأة بعد.");
                return;
            }
            const transaction = this.dbInstance.transaction(["pendingSyncLogs"], "readonly");
            const store = transaction.objectStore("pendingSyncLogs");
            const request = store.getAll();

            request.onsuccess = () => {
                resolve(request.result);
            };

            request.onerror = (event) => {
                reject(event.target.error);
            };
        });
    }
};

// تشغيل قاعدة البيانات فور تحميل الملف
document.addEventListener("DOMContentLoaded", function() {
    AppDatabase.initDatabase();
});