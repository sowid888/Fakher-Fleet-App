package com.fakher.truck2600;

import android.content.Context;
import android.content.SharedPreferences;

public class SessionManager {

    private static final String PREF_NAME = "Truck2600Session";
    private static final String KEY_VEHICLE_ID = "vehicle_id";
    private static final String KEY_DRIVER_NAME = "driver_name";
    private static final String KEY_PIN_CODE = "pin_code";
    private static final String KEY_IS_REGISTERED = "is_registered";

    private final SharedPreferences pref;
    private final SharedPreferences.Editor editor;

    public SessionManager(Context context) {
        pref = context.getSharedPreferences(PREF_NAME, Context.MODE_PRIVATE);
        editor = pref.edit();
    }

    /**
     * حفظ بيانات المركبة والسائق والرمز السري لأول مرة عند تسجيل الدخول
     */
    public void saveSession(String vehicleId, String driverName, String pinCode) {
        editor.putString(KEY_VEHICLE_ID, vehicleId);
        editor.putString(KEY_DRIVER_NAME, driverName);
        editor.putString(KEY_PIN_CODE, pinCode);
        editor.putBoolean(KEY_IS_REGISTERED, true);
        editor.apply();
    }

    /**
     * جلب رقم المركبة المحفوظ
     */
    public String getVehicleId() {
        return pref.getString(KEY_VEHICLE_ID, "");
    }

    /**
     * جلب اسم السائق المحفوظ
     */
    public String getDriverName() {
        return pref.getString(KEY_DRIVER_NAME, "");
    }

    /**
     * جلب الرمز السري المحفوظ
     */
    public String getPinCode() {
        return pref.getString(KEY_PIN_CODE, "");
    }

    /**
     * التحقق هل الجهاز مفعل برمز سري مسبقاً أم لا
     */
    public boolean isRegistered() {
        return pref.getBoolean(KEY_IS_REGISTERED, false);
    }

    /**
     * مسح البيانات وإلغاء التفعيل (عند تغيير الرمز السري من قبل مشغل النظام)
     */
    public void clearSession() {
        editor.clear();
        editor.apply();
    }
}