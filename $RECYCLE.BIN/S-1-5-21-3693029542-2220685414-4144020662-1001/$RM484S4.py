import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

void main() {
  runApp(FakherSovereignApp());
}

class FakherSovereignApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'منظومة فاخر السيادية 2600',
      theme: ThemeData(
        brightness: Brightness.dark,
        primaryColor: Color(0xFF0F172A),
        scaffoldBackgroundColor: Color(0xFF020617),
        fontFamily: 'Arial',
      ),
      home: LoginScreen(),
      debugShowCheckedModeBanner: false,
    );
  }
}

// =========================================================================
// 1. شاشة تسجيل الدخول والمطابقة الآلية
// =========================================================================
class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _nameController = TextEditingController();
  final TextEditingController _plateController = TextEditingController();
  final TextEditingController _phoneController = TextEditingController();

  // سيتم ربط هذا الرابط ديناميكياً مع سيرفر الحاسوب لاحقاً
  final String baseUrl = "http://fakher2600.pagekite.me"; 

  void _loginAndMatch() {
    if (_formKey.currentState!.validate()) {
      String fullName = _nameController.text.trim();
      String plateNumber = _plateController.text.trim();
      String phoneNumber = _phoneController.text.trim();

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('⏳ جاري جلب معطيات المطابقة الآلية من الخزنة المركزية...')),
      );

      // ذكاء اصطناعي مبسط لفرز الأسطول (شاحنات / سيارات)
      bool isTruck = plateNumber.contains("شاحنة") || plateNumber.startsWith("1");

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => DriverDashboard(
            driverName: fullName,
            plateNum: plateNumber,
            phoneNumber: phoneNumber,
            vehicleType: isTruck ? "Truck" : "Car",
            baseUrl: baseUrl,
          ),
        ),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(24.0),
          child: Form(
            key: _formKey,
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Icon(Icons.shield, size: 80, color: Color(0xFF38BDF8)),
                SizedBox(height: 15),
                Text(
                  'منظومة فاخر السيادية 2600',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Color(0xFF38BDF8)),
                ),
                SizedBox(height: 40),
                TextFormField(
                  controller: _nameController,
                  decoration: InputDecoration(labelText: 'اسم السائق المعتمد رباعياً', border: OutlineInputBorder(), prefixIcon: Icon(Icons.person)),
                  validator: (value) => (value == null || value.isEmpty) ? 'يرجى إدخال الاسم' : null,
                ),
                SizedBox(height: 15),
                TextFormField(
                  controller: _plateController,
                  decoration: InputDecoration(labelText: 'رقم لوحة المركبة (مثال: 1234 شاحنة)', border: OutlineInputBorder(), prefixIcon: Icon(Icons.local_shipping)),
                  validator: (value) => (value == null || value.isEmpty) ? 'يرجى إدخال رقم اللوحة' : null,
                ),
                SizedBox(height: 15),
                TextFormField(
                  controller: _phoneController,
                  keyboardType: TextInputType.phone,
                  obscureText: false, // تم التعديل ليظهر الرقم بوضوح أثناء الإدخال
                  decoration: InputDecoration(labelText: 'رقم هاتف الواتساب', border: OutlineInputBorder(), prefixIcon: Icon(Icons.phone)),
                  validator: (value) => (value == null || value.isEmpty) ? 'يرجى إدخال رقم الهاتف' : null,
                ),
                SizedBox(height: 30),
                ElevatedButton(
                  onPressed: _loginAndMatch,
                  style: ElevatedButton.styleFrom(backgroundColor: Color(0xFF1E293B), padding: EdgeInsets.symmetric(vertical: 16)),
                  child: Text('تسجيل الدخول والمطابقة الآلية', style: TextStyle(fontSize: 16, color: Colors.white)),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}

// =========================================================================
// 2. لوحة التحكم الرئيسية للسائق
// =========================================================================
class DriverDashboard extends StatelessWidget {
  final String driverName;
  final String plateNum;
  final String phoneNumber;
  final String vehicleType;
  final String baseUrl;

  DriverDashboard({
    required this.driverName, 
    required this.plateNum, 
    required this.phoneNumber,
    required this.vehicleType, 
    required this.baseUrl
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('لوحة قيادة الأسطول المركزي'), backgroundColor: Color(0xFF0F172A), centerTitle: true),
      body: Padding(
        padding: EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Container(
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(color: Color(0xFF1E293B), borderRadius: BorderRadius.circular(12), border: Border.all(color: Color(0xFF38BDF8), width: 1)),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('👤 السائق: $driverName', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  SizedBox(height: 6),
                  Text('🔢 رقم اللوحة: $plateNum', style: TextStyle(fontSize: 14, color: Colors.grey[300])),
                  SizedBox(height: 6),
                  Text('⚙️ القطاع: ${vehicleType == "Truck" ? "🚛 قطاع الشاحنات" : "🚗 قطاع السيارات"}', style: TextStyle(fontSize: 14, color: Color(0xFF4ADE80))),
                ],
              ),
            ),
            SizedBox(height: 30),
            _buildMenuButton(context, Icons.speed, 'إرسال قراءة العداد الحالي', Color(0xFF2563EB), () => Navigator.push(context, MaterialPageRoute(builder: (context) => OdometerScreen(driverName: driverName, plateNum: plateNum, vehicleType: vehicleType, baseUrl: baseUrl)))),
            SizedBox(height: 15),
            _buildMenuButton(context, Icons.build, 'البلاغ الفوري عن عطل ميكانيكي', Color(0xFFDC2626), () => Navigator.push(context, MaterialPageRoute(builder: (context) => FaultReportScreen(driverName: driverName, plateNum: plateNum, vehicleType: vehicleType, baseUrl: baseUrl)))),
            SizedBox(height: 15),
            _buildMenuButton(context, Icons.vpn_key, 'كرت التفعيل والرموز', Color(0xFFD97706), () => Navigator.push(context, MaterialPageRoute(builder: (context) => SecurityActivationScreen(driverName: driverName, plateNum: plateNum, baseUrl: baseUrl)))),
          ],
        ),
      ),
    );
  }

  Widget _buildMenuButton(BuildContext context, IconData icon, String title, Color color, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(10),
      child: Container(
        padding: EdgeInsets.symmetric(vertical: 20, horizontal: 16),
        decoration: BoxDecoration(color: color.withOpacity(0.15), borderRadius: BorderRadius.circular(10), border: Border.all(color: color, width: 1.5)),
        child: Row(
          children: [
            Icon(icon, size: 30, color: color),
            SizedBox(width: 15),
            Expanded(child: Text(title, style: TextStyle(fontSize: 15, fontWeight: FontWeight.bold, color: Colors.white))),
            Icon(Icons.arrow_forward_ios, size: 16, color: Colors.grey),
          ],
        ),
      ),
    );
  }
}

// =========================================================================
// 3. واجهة إرسال العداد الحالي
// =========================================================================
class OdometerScreen extends StatefulWidget {
  final String driverName;
  final String plateNum;
  final String vehicleType;
  final String baseUrl;

  OdometerScreen({required this.driverName, required this.plateNum, required this.vehicleType, required this.baseUrl});

  @override
  _OdometerScreenState createState() => _OdometerScreenState();
}

class _OdometerScreenState extends State<OdometerScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _kmController = TextEditingController();

  void _submitOdometer() async {
    if (_formKey.currentState!.validate()) {
      double enteredKm = double.parse(_kmController.text.trim());
      
      Map<String, dynamic> data = {
        'driver_name': widget.driverName,
        'plate_num': widget.plateNum,
        'vehicle_type': widget.vehicleType, // تمرير نوع المركبة لذكاء السيرفر
        'odo_reading': enteredKm,
        'message_type': 'قراءة عداد روتينية',
      };

      try {
        final response = await http.post(
          Uri.parse('${widget.baseUrl}/api/driver/message'),
          headers: {'Content-Type': 'application/json; charset=UTF-8'},
          body: jsonEncode(data),
        );

        if (response.statusCode == 200) {
          final resData = jsonDecode(response.body);
          if (resData['status'] == '🚨 TAMPERED') {
            _showFeedbackDialog("⚠️ تلاعب بالقراءة", "القراءة غير منطقية ومخالفة للمسجّل.", Colors.red);
          } else {
            _showFeedbackDialog("✅ قيد ناجح", "تم التوثيق بنجاح في النظام المركزي.", Colors.green);
            _kmController.clear();
          }
        } else {
          _showFeedbackDialog("❌ فشل السيرفر", "السيرفر لم يستجب، كود الخطأ: ${response.statusCode}", Colors.orange);
        }
      } catch (e) {
        _showFeedbackDialog("📦 خطأ شبكة", "تأكد من اتصال الحاسوب الرئيسي وتشغيل سيرفر البايثون المحلي.", Colors.red);
      }
    }
  }

  void _showFeedbackDialog(String title, String content, Color titleColor) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(title, style: TextStyle(color: titleColor, fontWeight: FontWeight.bold)),
        content: Text(content),
        actions: [TextButton(onPressed: () => Navigator.pop(context), child: Text('موافق'))],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('توثيق قراءة العداد')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                controller: _kmController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(labelText: 'قراءة العداد الحالية (KM)', border: OutlineInputBorder(), prefixIcon: Icon(Icons.speed)),
                validator: (value) => (value == null || value.isEmpty) ? 'يرجى كتابة أرقام صحيحة' : null,
              ),
              SizedBox(height: 25),
              ElevatedButton(
                onPressed: _submitOdometer,
                style: ElevatedButton.styleFrom(backgroundColor: Color(0xFF2563EB), padding: EdgeInsets.symmetric(vertical: 15)),
                child: Text('إرسال القراءة للعمليات', style: TextStyle(color: Colors.white, fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// =========================================================================
// 4. واجهة بلاغات الأعطال الفنية
// =========================================================================
class FaultReportScreen extends StatefulWidget {
  final String driverName;
  final String plateNum;
  final String vehicleType;
  final String baseUrl;

  // تم توحيد الرابط والمقاييس ليتناسب مع أسطول السيارات والشاحنات معاً
  FaultReportScreen({required this.driverName, required this.plateNum, required this.vehicleType, required this.baseUrl});

  @override
  _FaultReportScreenState createState() => _FaultReportScreenState();
}

class _FaultReportScreenState extends State<FaultReportScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _detailController = TextEditingController();
  String _selectedCategory = 'عطل في المحرك / ميكانيك';
  final List<String> _categories = ['عطل في المحرك / ميكانيك', 'عطل في الكهرباء والأنظمة', 'مشكلة في الإطارات / الهيدروليك', 'أعطال المكابح / الفرامل والأمان', 'أخرى'];

  void _sendFaultLog() async {
    if (_formKey.currentState!.validate()) {
      try {
        final response = await http.post(
          Uri.parse('${widget.baseUrl}/api/fleet/fault'), // تم تعديل الرابط ليكون عاماً للأسطول (fleet) بدلاً من تخصيص الشاحنات فقط لتسهيل الربط
          headers: {'Content-Type': 'application/json; charset=UTF-8'},
          body: jsonEncode({
            'driver_name': widget.driverName,
            'plate_num': widget.plateNum,
            'vehicle_type': widget.vehicleType,
            'fault_category': _selectedCategory,
            'fault_detail': _detailController.text.trim(),
          }),
        );
        if (response.statusCode == 200) {
          showDialog(
            context: context, 
            builder: (context) => AlertDialog(
              title: Text('✅ تم التوثيق'), 
              content: Text('تم إرسال بلاغ العطل بنجاح لغرفة إدارة الحركة!'), 
              actions: [TextButton(onPressed: () { Navigator.pop(context); Navigator.pop(context); }, child: Text('موافق'))]
            )
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('❌ خطأ في السيرفر الرئيسي.')));
        }
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('❌ تعذر الاتصال، تأكد من تشغيل نفق الاتصال بالسيرفر.')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('الإبلاغ الفوري عن عطل')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              DropdownButtonFormField<String>(value: _selectedCategory, decoration: OutlineInputBorder(), items: _categories.map((cat) => DropdownMenuItem(value: cat, child: Text(cat))).toList(), onChanged: (val) => setState(() => _selectedCategory = val!)),
              SizedBox(height: 20),
              TextFormField(controller: _detailController, maxLines: 4, decoration: InputDecoration(labelText: 'تفاصيل العطل والقطع المتضررة...', border: OutlineInputBorder()), validator: (value) => (value == null || value.isEmpty) ? 'يرجى كتابة التفاصيل' : null),
              SizedBox(height: 25),
              ElevatedButton(onPressed: _sendFaultLog, style: ElevatedButton.styleFrom(backgroundColor: Color(0xFFDC2626), padding: EdgeInsets.symmetric(vertical: 15)), child: Text('إرسال بلاغ فوري وعاجل', style: TextStyle(color: Colors.white))),
            ],
          ),
        ),
      ),
    );
  }
}

// =========================================================================
// 5. واجهة كرت التفعيل ومطابقة الرموز
// =========================================================================
class SecurityActivationScreen extends StatefulWidget {
  final String driverName;
  final String plateNum;
  final String baseUrl;

  SecurityActivationScreen({required this.driverName, required this.plateNum, required this.baseUrl});

  @override
  _SecurityActivationScreenState createState() => _SecurityActivationScreenState();
}

class _SecurityActivationScreenState extends State<SecurityActivationScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _codeController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('مركز التراخيص السيادية')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch2222222222222222222222222222222222222222222222222222222222222igator.pop(context), style: ElevatedButton.styleFrom(backgroundColor: Color(0xFFD97706)), child: Text('تفعيل الهوية الرقمية للمركبة', style: TextStyle(color: Colors.white))),
            ],
          ),
        ),
      ),
    );
  }
}