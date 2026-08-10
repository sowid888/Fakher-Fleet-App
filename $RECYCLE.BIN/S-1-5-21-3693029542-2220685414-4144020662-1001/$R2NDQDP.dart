import 'package:flutter/material.dart';

void main() {
  runApp(const SafeDriverApp());
}

class SafeDriverApp extends StatelessWidget {
  const SafeDriverApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'بوابة السائقين النظيفة',
      home: Scaffold(
        appBar: AppBar(
          title: const Text('نظام المطابقة والربط الجديد'),
          backgroundColor: Colors.teal,
        ),
        body: const Center(
          child: Text(
            '🚀 تم إنشاء الملف الجديد بنجاح وبدون أخطاء!',
            style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
        ),
      ),
    );
  }
}