import json
from Receiver import clean_input, find_best_match_with_score

class AcrossMenaBrain:
    def __init__(self):
        self.db_path = "knowledge_base.json"

    def generate_image_url(self, hs_code):
        # سنستخدم رابطاً ديناميكياً يعتمد على رقم البند الجمركي
        # هذا مثال لرابط من قاعدة بيانات جمركية عالمية
        return f"https://www.customs.gov.sy/images/items/{hs_code}.jpg"

    def ask(self, user_query):
        # 1. المعالجة في طبقة الاستقبال
        cleaned = clean_input(user_query)
        match = find_best_match_with_score(cleaned)

        if not match or match['confidence_score'] < 30:
            return "عذراً يا عيسى، لم أستطع فهم المنتج بدقة. هل يمكنك المحاولة باسم آخر؟"

        # 2. استخراج البيانات
        name = match['material_clean']
        hs_code = match['hs6_global']
        price = match.get('priceFull', 'غير متوفر حالياً')
        confidence = match['confidence_score']
        
        # 3. صياغة الرد الاحترافي
        response = f"""
📦 **المنتج:** {name}
🔢 **البند الجمركي:** {hs_code}
💰 **التكلفة التقديرية:** {price}
🎯 **دقة المطابقة:** {confidence}%

🖼️ **صورة المنتج المقترحة:** {self.generate_image_url(hs_code)}

💡 **نصيحة عبر مينا:** تأكد من مطابقة المواصفات الفنية للبند {hs_code} قبل الشحن.
        """
        return response

# --- تجربة العقل الآن ---
brain = AcrossMenaBrain()
print(brain.ask("بدي استورد موتورات"))
