import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:io'; // 🟢 مكتبة مدمجة أساسية في النظام لا تسبب أي ألوان حمراء

void main() {
  runApp(const DriverApp());
}

class DriverApp extends StatelessWidget {
  const DriverApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'بوابة السائقين السيادية',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: const DriverHomeScreen(),
    );
  }
}

class DriverHomeScreen extends StatefulWidget {
  const DriverHomeScreen({Key? key}) : super(key: key);

  @override
  State<DriverHomeScreen> createState() => _DriverHomeScreenState();
}

class _DriverHomeScreenState extends State<DriverHomeScreen> {
  // 1. المتغير المركزي الموحد للربط بالنفق الفعلي
  final String sovereignBaseUrl = "http://fakher2600.pagekite.me"; 

  // 2. دالة الإرسال المحصنة بالمكتبة المدمجة
  Future<void> sendDataToCentralVault(String endpoint, Map<String, dynamic> data) async {
    final url = Uri.parse('$sovereignBaseUrl$endpoint');
    final httpClient = HttpClient();
    
    try {
      // فتح الاتصال عبر المكتبة الأساسية للنظام
      final request = await httpClient.postUrl(url)
          .timeout(const Duration(seconds: 15));
          
      request.headers.set('content-type', 'application/json; charset=UTF-8');
      request.add(utf8.encode(jsonEncode(data)));
      
      final response = await request.close();

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("✅ تم المزامنة والرفع بنجاح")),
        );
      } else {
        print("⚠️ خطأ في الاستجابة المركزية: ${response.statusCode}");
      }
    } catch (e) {
      print("❌ فشل الارتباط بالنفق المفتوح: $e");
    } finally {
      httpClient.close();
    }
  }

  @override
  Widget build(BuildContext cont
          child: const Text('إرسال نبضة فحص للنفق المركزي'),
        ),
      ),
    );
  }
}لللل