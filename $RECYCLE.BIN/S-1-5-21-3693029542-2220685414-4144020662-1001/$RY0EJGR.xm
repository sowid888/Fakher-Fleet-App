<?xml version='1.0' encoding='utf-8'?>
<widget id="com.aljozi.fleetapp" version="1.0.0" xmlns="http://www.w3.org/ns/widgets" xmlns:cdv="http://cordova.apache.org/ns/1.0">
    
    <!-- اسم التطبيق الظاهر على الهاتف -->
    <name>مؤسسة الجوزي - قطاع الحركة والنقل</name>
    
    <!-- وصف التطبيق -->
    <description>
        نظام الجوزي لإدارة الأسطول والمتابعة الميدانية للعدادات والبلاغات.
    </description>
    
    <!-- الصفحة الرئيسية للانطلاق -->
    <content src="index.html" />
    
    <!-- الصلاحيات والتصاريح المطلوبة (الكاميرا، الموقع، الإنترنت) -->
    <access origin="*" />
    <allow-intent href="http://*/*" />
    <allow-intent href="https://*/*" />
    
    <platform name="android">
        <preference name="Orientation" value="portrait" />
        <config-file target="AndroidManifest.xml" parent="/*">
            <uses-permission android:name="android.permission.INTERNET" />
            <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
            <uses-permission android:name="android.permission.CAMERA" />
            <uses-permission android:name="android.permission.RECORD_AUDIO" />
            <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
            <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />
        </config-file>
    </platform>
    
</widget>