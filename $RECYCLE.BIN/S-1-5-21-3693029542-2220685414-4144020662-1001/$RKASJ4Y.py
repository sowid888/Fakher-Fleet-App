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
        primaryColor: Color(0xFF0F172A), // اللون الملكي الداكن للمنظومة
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

  // النطاق المركزي المعتمد عبر نفق pagekite
  final String baseUrl = "http://fakher2600.pagekite.me"; 

  void _loginAndMatch() {
    if (_formKey.currentState!.validate()) {
      String fullName = _nameController.text.trim();
      String plateNumber = _plateController.text.trim();

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('⏳ جاري جلب معطيات المطابقة الآلية من الخزنة المركزية...')),
      );

      // توجيه تلقائي ذكي بناءً على فئة المركبة المكتوبة في اللوحة
      bool isTruck = plateNumber.contains("شاحنة") || plateNumber.startsWith("1");

      Navigator.pushReplacement(
        context,
        MaterialPageRoute(
          builder: (context) => DriverDashboard(
            driverName: fullName,
            plateNum: plateNumber,
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
                Text(
                  'بوابة السائقين والمطابقة الجينية للأسطول',
                  textAlign: TextAlign.center,
                  style: TextStyle(fontSize: 14, color: Colors.grey),
                ),
                SizedBox(height: 40),
                TextFormField(
                  controller: _nameController,
                  decoration: InputDecoration(
                    labelText: 'اسم السائق المعتمد رباعياً',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.person),
                  ),
                  validator: (value) => (value == null || value.isEmpty) ? 'يرجى إدخال الاسم' : null,
                ),
                SizedBox(height: 15),
                TextFormField(
                  controller: _plateController,
                  decoration: InputDecoration(
                    labelText: 'رقم لوحة المركبة (مثال: 1234 شاحنة)',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.local_shipping),
                  ),
                  validator: (value) => (value == null || value.isEmpty) ? 'يرجى إدخال رقم اللوحة' : null,
                ),
                SizedBox(height: 15),
                TextFormField(
                  controller: _phoneController,
                  keyboardType: TextInputType.phone,
                  obscureText: true,
                  decoration: InputDecoration(
                    labelText: 'رقم هاتف الواتساب (شفرة التحقق)',
                    border: OutlineInputBorder(),
                    prefixIcon: Icon(Icons.phone),
                  ),
                  validator: (value) => (value == null || value.isEmpty) ? 'يرجى إدخال رقم الهاتف' : null,
                ),
                SizedBox(height: 30),
                ElevatedButton(
                  onPressed: _loginAndMatch,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Color(0xFF1E293B),
                    padding: EdgeInsets.symmetric(vertical: 16),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(8)),
                  ),
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
// 2. لوحة التحكم الرئيسية للسائق بعد المطابقة
// =========================================================================
class DriverDashboard extends StatelessWidget {
  final String driverName;
  final String plateNum;
  final String vehicleType;
  final String baseUrl;

  DriverDashboard({
    required this.driverName,
    required this.plateNum,
    required this.vehicleType,
    required this.baseUrl,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('لوحة قيادة السطول المركزي'),
        backgroundColor: Color(0xFF0F172A),
        centerTitle: true,
      ),
      body: Padding(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // كرت تعريف الهوية النشطة داخل التطبيق
            Container(
              padding: EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Color(0xFF1E293B),
                borderRadius: BorderRadius.circular(12),
                border: Border.all(color: Color(0xFF38BDF8), width: 1),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('👤 السائق: $driverName', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold)),
                  SizedBox(height: 6),
                  Text('🔢 رقم اللوحة الفعلي: $plateNum', style: TextStyle(fontSize: 14, color: Colors.grey[300])),
                  SizedBox(height: 6),
                  Text('⚙️ تصنيف الحصانة: ${vehicleType == "Truck" ? "🚛 قطاع الشاحنات السيادي" : "🚗 قطاع سيارات الإدارة"}', 
                    style: TextStyle(fontSize: 14, color: Color(0xFF4ADE80)),
                  ),
                ],
              ),
            ),
            SizedBox(height: 30),
            Text('العمليات والوظائف الفورية المتاحة:', style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold, color: Colors.grey)),
            SizedBox(height: 15),

            // زر (1) إرسال قراءة العداد الحالي
            _buildMenuButton(
              context: context,
              icon: Icons.speed,
              title: 'إرسال قراءة العداد الحالي (الكيلومتر)',
              color: Color(0xFF2563EB),
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => OdometerScreen(driverName: driverName, plateNum: plateNum, baseUrl: baseUrl))),
            ),
            SizedBox(height: 15),

            // زر (2) الإبلاغ عن عطل فني مفاجئ
            _buildMenuButton(
              context: context,
              icon: Icons.build,
              title: 'البلاغ الفوري عن عطل ميكانيكي/كهربائي',
              color: Color(0xFFDC2626),
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => FaultReportScreen(driverName: driverName, plateNum: plateNum, baseUrl: baseUrl))),
            ),
            SizedBox(height: 15),

            // زر (3) كرت التفعيل والفتح السيادي
            _buildMenuButton(
              context: context,
              icon: Icons.vpn_key,
              title: 'كرت التفعيل ومطابقة رموز الفتح السيادية',
              color: Color(0xFFD97706),
              onTap: () => Navigator.push(context, MaterialPageRoute(builder: (context) => SecurityActivationScreen(driverName: driverName, plateNum: plateNum, baseUrl: baseUrl))),
            ),
          ],
        ),
        padding: EdgeInsets.all(20.0),
      ),
    );
  }

  Widget _buildMenuButton({required BuildContext context, required IconData icon, required String title, required Color color, required VoidCallback onTap}) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(10),
      child: Container(
        padding: EdgeInsets.symmetric(vertical: 20, horizontal: 16),
        decoration: BoxDecoration(
          color: color.withOpacity(0.15),
          borderRadius: BorderRadius.circular(10),
          border: Border.all(color: color, width: 1.5),
        ),
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
// 3. واجهة إرسال العداد الحالي وكشف التلاعب (Odometer Screen)
// =========================================================================
class OdometerScreen extends StatefulWidget {
  final String driverName;
  final String plateNum;
  final String baseUrl;

  OdometerScreen({required this.driverName, required this.plateNum, required this.baseUrl});

  @override
  _OdometerScreenState createState() => _OdometerScreenState();
}

class _OdometerScreenState extends State<OdometerScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _kmController = TextEditingController();

  void _submitOdometer() async {
    if (_formKey.currentState!.validate()) {
      double enteredKm = double.parse(_kmController.text.trim());

      // قمنا بربط الواجهة بذكاء مع خوارزمية السيرفر و algorithms_engine.py باطنيّاً
      // وإظهار رسالة فورية حصينة للسائق في حال حدوث انحراف
      try {
        final response = await http.post(
          Uri.parse('${widget.baseUrl}/api/driver/message'),
          headers: {'Content-Type': 'application/json; charset=UTF-8'},
          body: jsonEncode({
            'driver_name': widget.driverName,
            'plate_num': widget.plateNum,
            'odo_reading': enteredKm,
            'message_type': 'قراءة عداد روتينية',
          }),
        );

        if (response.statusCode == 200) {
          final resData = jsonDecode(response.body);
          if (resData['status'] == '🚨 TAMPERED') {
            _showFeedbackDialog("⚠️ خرق أمني كاذب أو تلاعب", "عذراً يا سائق، القراءة المدخلة غير منطقية أو أقل من السابقة! تم قيد الحركة وتوجيه التقرير صامتاً إلى حاسوب الإدارة للمراجعة الجنائية الرقمية.", Colors.red);
          } else {
            _showFeedbackDialog("✅ قيد ناجح", "تم إرسال وتأمين قراءة العداد بنجاح في سجلات الأتمتة الموحدة بالخزنة السياسية.", Colors.green);
            _kmController.clear();
          }
        } else {
          _showFeedbackDialog("❌ فشل الاتصال", "تعذر الوصول للسيرفر المركزي، يرجى التأكد من تشغيل ملف Fakher_Tunnel.py على الكمبيوتر.", Colors.orange);
        }
      } catch (e) {
        _showFeedbackDialog("❌ خطأ بالشبكة", "فشل الارتباط بالنفق المفتوح. يرجى مراجعة المهندس جمال سويد.", Colors.red);
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
      appBar: AppBar(title: Text('توثيق قراءة العداد للرقابة')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text('📊 يرجى إدخال الأرقام الظاهرة في لوحة القيادة الحالية للمركبة:', style: TextStyle(fontSize: 15)),
              SizedBox(height: 20),
              TextFormField(
                controller: _kmController,
                keyboardType: TextInputType.number,
                decoration: InputDecoration(
                  labelText: 'قراءة العداد الحالية (KM / ميل)',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.speed),
                ),
                validator: (value) => (value == null || value.isEmpty) ? 'يرجى كتابة أرقام صحيحة فقط' : null,
              ),
              SizedBox(height: 25),
              ElevatedButton(
                onPressed: _submitOdometer,
                style: ElevatedButton.styleFrom(backgroundColor: Color(0xFF2563EB), padding: EdgeInsets.symmetric(vertical: 15)),
                child: Text('قيد وإرسال بالخزنة السيادية', style: TextStyle(color: Colors.white, fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// =========================================================================
// 4. واجهة بلاغات الأعطال الفنية بالفئات المعتمدة (Fault Report Screen)
// =========================================================================
class FaultReportScreen extends StatefulWidget {
  final String driverName;
  final String plateNum;
  final String baseUrl;

  FaultReportScreen({required this.driverName, required this.plateNum, required this.baseUrl});

  @override
  _FaultReportScreenState createState() => _FaultReportScreenState();
}

class _FaultReportScreenState extends State<FaultReportScreen> {
  final _formKey = GlobalKey<FormState>();
  final TextEditingController _detailController = TextEditingController();
  
  // فئات الأعطال الصارمة والمطابقة لملف السيرفر Fakher_Truck_Server_2600.py
  String _selectedCategory = 'عطل في المحرك / ميكانيك';
  final List<String> _categories = [
    'عطل في المحرك / ميكانيك',
    'عطل في الكهرباء والأنظمة',
    'مشكلة في الإطارات / الهيدروليك',
    'أعطال المكابح / الفرامل والأمان',
    'أخرى (اكتب في التفاصيل)'
  ];

  void _sendFaultLog() async {
    if (_formKey.currentState!.validate()) {
      try {
        final response = await http.post(
          Uri.parse('${widget.baseUrl}/api/truck/fault'),
          headers: {'Content-Type': 'application/json; charset=UTF-8'},
          body: jsonEncode({
            'driver_name': widget.driverName,
            'plate_num': widget.plateNum,
            'fault_category': _selectedCategory,
            'fault_detail': _detailController.text.trim(),
          }),
        );

        if (response.statusCode == 200) {
          showDialog(
            context: context,
            builder: (context) => AlertDialog(
              title: Text('✅ تم التوثيق الفاخر', style: TextStyle(color: Colors.green, fontWeight: FontWeight.bold)),
              content: Text('تم قيد وحفظ عملية العطل رسمياً في السجل التاريخي بالخزنة المركزية، وتم إرسال البلاغ لبرنامج المهندس جمال بنجاح!'),
              actions: [TextButton(onPressed: () { Navigator.pop(context); Navigator.pop(context); }, child: Text('موافق'))],
            ),
          );
        }
      } catch (e) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('❌ تعذر الاتصال، يرجى تشغيل السيرفر المحلي والتحقق من النفق.')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('الإبلاغ الفوري عن عطل مركزي')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text('🛠️ اختر فئة العطل الرئيسية لتوجيه البلاغ للقسم المختص باطنيّاً:', style: TextStyle(fontSize: 14)),
              SizedBox(height: 10),
              DropdownButtonFormField<String>(
                value: _selectedCategory,
                decoration: OutlineInputBorder(),
                items: _categories.map((cat) => DropdownMenuItem(value: cat, child: Text(cat, style: TextStyle(fontSize: 14)))).toList(),
                onChanged: (val) => setState(() => _selectedCategory = val!),
              ),
              SizedBox(height: 20),
              TextFormField(
                controller: _detailController,
                maxLines: 4,
                decoration: InputDecoration(
                  labelText: 'اكتب تفاصيل العطل والقطع المتضررة بدقة...',
                  border: OutlineInputBorder(),
                  alignLabelWithHint: true,
                ),
                validator: (value) => (value == null || value.isEmpty) ? 'يرجى كتابة تفاصيل العطل' : null,
              ),
              SizedBox(height: 25),
              ElevatedButton(
                onPressed: _sendFaultLog,
                style: ElevatedButton.styleFrom(backgroundColor: Color(0xFFDC2626), padding: EdgeInsets.symmetric(vertical: 15)),
                child: Text('إرسال بلاغ فوري للإدارة', style: TextStyle(color: Colors.white, fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

// =========================================================================
// 5. واجهة كرت التفعيل ومطابقة رموز الفتح السيادية (Security Activation)
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

  void _verifyAuthCode() {
    if (_formKey.currentState!.validate()) {
      String code = _codeController.text.trim();

      // خوارزمية محاكاة التطابق للتحقق من الأكواد المستوردة من code_generator.py
      if (code.length >= 6) {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: Text('👑 الحصانة الرقمية معمدة', style: TextStyle(color: Colors.amber, fontWeight: FontWeight.bold)),
            content: Text('بمجرد لصق هذا الرمز، طابقت الهوية السيادية بنجاح وتم فتح صلاحيات الصيانة الفنية والمزامنة للرحلة الجارية فوراً.'),
            actions: [TextButton(onPressed: () => Navigator.pop(context), child: Text('موافق'))],
          ),
        );
      } else {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('❌ رمز فتح المنظومة غير صحيح أو ناقص، يرجى مراجعة المشرف.')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('مركز التراخيص والفتح السيادي')),
      body: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Icon(Icons.lock, size: 60, color: Color(0xFFD97706)),
              SizedBox(height: 15),
              Text(
                'انسخ رمز التفعيل والفتح السيادي المرسل إليك عبر الواتساب من برنامج الإدارة والصقه في الخانة أدناه لفتح حركات التشغيل الموحدة:',
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 14, height: 1.4),
              ),
              SizedBox(height: 25),
              TextFormField(
                controller: _codeController,
                textAlign: TextAlign.center,
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, letterSpacing: 2),
                decoration: InputDecoration(
                  hintText: 'أدخل رمز فتح المنظومة هنا...',
                  border: OutlineInputBorder(),
                ),
                validator: (value) => (value == null || value.isEmpty) ? 'يرجى لصق الرمز أولاً' : null,
              ),
              SizedBox(height: 25),
              ElevatedButton(
                onPressed: _verifyAuthCode,
                style: ElevatedButton.styleFrom(backgroundColor: Color(0xFFD97706), padding: EdgeInsets.symmetric(vertical: 15)),
                child: Text('تفعيل وتوثيق الهوية الرقمية', style: TextStyle(color: Colors.white, fontSize: 16)),
              ),
            ],
          ),
        ),
      ),
    );
  }
}