/**
 * مؤسسة الجوزي - قطاع الحركة والنقل
 * ملف التهيئة الرئيسي وإدارة المزامنة الدورية في الخلفية
 * بديل (FleetApplication.kt)
 */

const FleetApplication = {

    // فترات المزامنة الدورية بالدقائق (طابق 15 دقيقة من الملف الأصلي)
    SYNC_INTERVAL_MINUTES: 15,
    SYNC_WORK_NAME: "FleetDataSyncWork",

    // تشغيل التطبيق وتهيئة المزامنة
    init: function() {
        console.log("تم تشغيل تطبيق الجوزي لإدارة الأسطول...");
        this.setupBackgroundSync();
    },

    /**
     * جدولة مهمة المزامنة الدورية في الخلفية عند توفر شبكة الإنترنت
     */
    setupBackgroundSync: function() {
        console.log("إعداد جدولة المزامنة الدورية كل 15 دقيقة عند توفر الإنترنت...");

        // التحقق من حالة الشبكة وإجراء مزامنة فورية إن أمكن
        if (navigator.onLine) {
            this.executeSyncWorker();
        }

        // الاستماع لتغيرات حالة الشبكة
        window.addEventListener('online', () => {
            console.log("تم الاتصال بالإنترنت - بدء المزامنة المعلقة تلقائياً.");
            this.executeSyncWorker();
        });

        // إعداد التكرار الدوري كل 15 دقيقة (15 * 60 * 1000 مللي ثانية)
        const intervalMs = this.SYNC_INTERVAL_MINUTES * 60 * 1000;
        setInterval(() => {
            if (navigator.onLine) {
                console.log("تطبيق جدولة المزامنة الدورية (FleetDataSyncWork)...");
                this.executeSyncWorker();
            } else {
                console.log("تأجيل المزامنة: لا يوجد اتصال بالإنترنت حالياً.");
            }
        }, intervalMs);
    },

    /**
     * تنفيذ عامل المزامنة (SyncWorker) لرفع البيانات المخزنة محلياً
     */
    executeSyncWorker: function() {
        if (typeof AppDatabase !== 'undefined' && AppDatabase.getPendingLogs) {
            AppDatabase.getPendingLogs()
                .then(pendingLogs => {
                    if (pendingLogs && pendingLogs.length > 0) {
                        console.log(`جاري مزامنة ${pendingLogs.length} سجل مع خادم الجوزي...`);
                        // إرسال البيانات للـ Server وحذفها محلياً بعد التأكيد
                    } else {
                        console.log("لا توجد سجلات معلقة للمزامنة.");
                    }
                })
                .catch(err => {
                    console.error("خطأ أثناء جلب سجلات المزامنة:", err);
                });
        }
    }
};

// تشغيل التهيئة والمزامنة فور تحميل النافذة
document.addEventListener("DOMContentLoaded", () => {
    FleetApplication.init();
});