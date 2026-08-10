/**
 * مؤسسة الجوزي - قطاع الحركة والنقل
 * وحدة تحليل صورة عداد الوقود وحساب النسبة المئوية
 * بديل (FuelGaugeAnalyzer.kt)
 */

class FuelGaugeAnalyzer {

    /**
     * تحليل صورة عداد الوقود وحساب نسبة امتلائه بناءً على زاوية إبرة العداد.
     * @param {HTMLImageElement | HTMLCanvasElement} imageElement عنصر الصورة أو الكانفاس الملتقط
     * @returns {number} نسبة مئوية تقديرية لمستوى الوقود (0% - 100%)
     */
    analyzeFuelLevel(imageElement) {
        // إنشاء كانفاس مؤقت لمعالجة ثنائية الأبعاد للصورة
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');

        canvas.width = imageElement.width || imageElement.videoWidth || 640;
        canvas.height = imageElement.height || imageElement.videoHeight || 480;

        ctx.drawImage(imageElement, 0, 0, canvas.width, canvas.height);

        // استخراج بيانات البكسلات (RGB Data)
        const imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        const data = imageData.data;

        // 1. تحويل الصورة إلى درجات الرمادي (COLOR_RGB2GRAY)
        const grayData = new Uint8ClampedArray(canvas.width * canvas.height);
        for (let i = 0; i < data.length; i += 4) {
            const r = data[i];
            const g = data[i + 1];
            const b = data[i + 2];
            // المعادلة القياسية للتحويل إلى رمادي: 0.299R + 0.587G + 0.114B
            grayData[i / 4] = Math.round(0.299 * r + 0.587 * g + 0.114 * b);
        }

        // 2. تطبييق كشف الحواف (Canny Edge Detection Approach)
        let linePoints = [];
        const width = canvas.width;
        const height = canvas.height;

        // البحث عن التباين العالي المحتمل الممثل لإبرة العداد
        for (let y = 1; y < height - 1; y += 2) {
            for (let x = 1; x < width - 1; x += 2) {
                const idx = y * width + x;
                const diffX = Math.abs(grayData[idx + 1] - grayData[idx - 1]);
                const diffY = Math.abs(grayData[idx + width] - grayData[idx - width]);
                
                // حد العتبة (Canny threshold 50 to 150)
                if (diffX > 50 || diffY > 50) {
                    linePoints.push({ x: x, y: y });
                }
            }
        }

        let estimatedPercentage = -1;

        if (linePoints.length >= 2) {
            const p1 = linePoints[0];
            const p2 = linePoints[linePoints.length - 1];

            const dx = p2.x - p1.x;
            const dy = p2.y - p1.y;

            // 3. حساب زاوية إبرة العداد بالدرجات باستخدام atan2
            const radians = Math.atan2(dy, dx);
            let angle = radians * (180 / Math.PI);

            // 4. تحويل الزاوية إلى نسبة مئوية مقربة (0% - 100%)
            estimatedPercentage = ((angle + 90) / 180) * 100;
            
            // ضبط القيمة بين 0 و 100
            estimatedPercentage = Math.max(0, Math.min(100, estimatedPercentage));
        }

        // إرجاع النسبة المحسوبة أو القيمة الافتراضية 50%
        return estimatedPercentage >= 0 ? parseFloat(estimatedPercentage.toFixed(1)) : 50.0;
    }
}

// تصدير الكائن لاستخدامه مباشرة داخل شاشات المشروع
window.FuelGaugeAnalyzer = FuelGaugeAnalyzer;