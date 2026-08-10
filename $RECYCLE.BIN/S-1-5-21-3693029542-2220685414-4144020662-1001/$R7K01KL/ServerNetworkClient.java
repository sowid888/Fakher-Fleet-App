package com.fakher.truck2600;

import android.content.Context;
import android.os.Handler;
import android.os.Looper;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import org.json.JSONObject;

public class ServerNetworkClient {

    private static final String SERVER_BASE_URL = "http://192.168.1.100:5000/api/odo_fuel_sync";

    public interface NetworkCallback {
        void onSuccess(String response);
        void onFailure(String errorMessage);
        void onUnauthorized(); // تنبيه يتم تفعيله إذا تم تغيير الرمز السري من مشغل النظام
    }

    /**
     * إرسال قراءات العداد والوقود مع الرمز السري واسم السائق إلى السيرفر الرئيسي
     */
    public static void sendOdoAndFuelData(final Context context, final String odoRead, final String fuelLevel, final NetworkCallback callback) {
        new Thread(new Runnable() {
            @Override
            public void run() {
                HttpURLConnection urlConnection = null;
                SessionManager session = new SessionManager(context);

                try {
                    URL url = new URL(SERVER_BASE_URL);
                    urlConnection = (HttpURLConnection) url.openConnection();
                    urlConnection.setRequestMethod("POST");
                    urlConnection.setRequestProperty("Content-Type", "application/json; utf-8");
                    urlConnection.setRequestProperty("Accept", "application/json");
                    urlConnection.setDoOutput(true);
                    urlConnection.setConnectTimeout(10000);
                    urlConnection.setReadTimeout(10000);

                    // 1. تجديد البيانات وتضمين الرمز السري واسم السائق تلقائياً من الذاكرة
                    JSONObject jsonParam = new JSONObject();
                    jsonParam.put("truck_id", session.getVehicleId());
                    jsonParam.put("driver_name", session.getDriverName());
                    jsonParam.put("pin_code", session.getPinCode());
                    jsonParam.put("odo_reading", odoRead);
                    jsonParam.put("fuel_level", fuelLevel);
                    jsonParam.put("timestamp", System.currentTimeMillis());

                    // 2. إرسال حزمة البيانات
                    try (OutputStream os = urlConnection.getOutputStream()) {
                        byte[] input = jsonParam.toString().getBytes(StandardCharsets.UTF_8);
                        os.write(input, 0, input.length);
                    }

                    // 3. التحقق من رد السيرفر
                    int responseCode = urlConnection.getResponseCode();

                    if (responseCode == HttpURLConnection.HTTP_OK || responseCode == HttpURLConnection.HTTP_CREATED) {
                        new Handler(Looper.getMainLooper()).post(new Runnable() {
                            @Override
                            public void run() {
                                callback.onSuccess("تم إرسال القراءات بنجاح إلى السيرفر الرئيسي.");
                            }
                        });
                    } else if (responseCode == HttpURLConnection.HTTP_UNAUTHORIZED) { 
                        // 4. إذا قام المدير بتغيير الرمز السري، السيرفر سيرد بـ 401، ونمسح الرمز القديم من الهاتف فوراً
                        session.clearSession();
                        new Handler(Looper.getMainLooper()).post(new Runnable() {
                            @Override
                            public void run() {
                                callback.onUnauthorized();
                            }
                        });
                    } else {
                        final String errorMsg = "خطأ في السيرفر! رمز الاستجابة: " + responseCode;
                        new Handler(Looper.getMainLooper()).post(new Runnable() {
                            @Override
                            public void run() {
                                callback.onFailure(errorMsg);
                            }
                        });
                    }

                } catch (final Exception e) {
                    new Handler(Looper.getMainLooper()).post(new Runnable() {
                        @Override
                        public void run() {
                            callback.onFailure("تعذر الاتصال بالسيرفر: " + e.getLocalizedMessage());
                        }
                    });
                } finally {
                    if (urlConnection != null) {
                        urlConnection.disconnect();
                    }
                }
            }
        }).start();
    }
}