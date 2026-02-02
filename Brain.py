import json
from Receiver import clean_input, find_best_match_with_score

class AcrossMenaBrain:
    def __init__(self):
        self.db_path = "knowledge_base.json"

    def ask(self, user_query):
        # 1. تنظيف وفهم المدخلات
        cleaned = clean_input(user_query)
        # 2. البحث في قاعدة البيانات
        match = find_best_match_with_score(cleaned, self.db_path)

        if not match:
            return "❌ عذراً يا عيسى، لم أجد هذه المادة في قاعدة البيانات."

        # 3. صياغة الرد
        name = match.get('material_clean', 'غير معروف')
        hs_code = match.get('hs6_global', '000000')
        price = match.get('priceFull', 'غير متوفر')
        confidence = match.get('confidence_score', 0)
        
        status = "✅ مؤكد" if confidence > 70 else "⚠️ تقريبي"

        response = f"""
🎯 نتيجة البحث لـ "Across MENA":
-------------------------------
📦 المنتج: {name}
🔢 البند الجمركي: {hs_code}
💰 السعر التقديري: {price}
📊 الدقة: {confidence}% ({status})
-------------------------------
        """
        return response

# الاختبار التشغيلي
if __name__ == "__main__":
    brain = AcrossMenaBrain()
    # جربنا كلمة موتورات لأننا وضعناها في القاموس
    print(brain.ask("بدي استورد موتورات"))
