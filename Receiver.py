import json
from difflib import get_close_matches

# 1. قاموس المرادفات (العقل المحلي)
SYRIAN_SYNONYMS = {
    "دواليب": "إطارات",
    "قداحة": "ولاعة",
    "براد": "ثلاجة",
    "موتور": "محرك",
    "بفلة": "إكسسوارات خرز",
    "شماسي": "مظلات مطر",
    "بطاريات جيل": "مدخرات كهربائية",
    "راوتر": "أجهزة إرسال بيانات"
}

def clean_input(user_query):
    # تنظيف النص وتوحيد التنسيق
    query = user_query.strip().lower()
    
    # تبديل الكلمات العامية بالرسمية
    words = query.split()
    translated_words = [SYRIAN_SYNONYMS.get(w, w) for w in words]
    return " ".join(translated_words)

def find_best_match(query, database_path="knowledge_base.json"):
    try:
        with open(database_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        # استخراج قائمة المواد من قاعدة بياناتك
        materials_list = [item['material_clean'] for item in data]
        
        # البحث عن أقرب تطابق (حتى لو في أخطاء إملائية)
        matches = get_close_matches(query, materials_list, n=1, cutoff=0.3)
        
        if matches:
            # العودة بالسطر الكامل للمادة من البيانات
            result = next(item for item in data if item['material_clean'] == matches[0])
            return result
        return None
    except Exception as e:
        return f"Error: {e}"

# --- تجربة التشغيل ---
user_ask = "بدي سعر دواليب سيارات"
processed_query = clean_input(user_ask)
match = find_best_match(processed_query)

if match:
    print(f"✅ تم الفهم! تقصد: {match['material_clean']}")
    print(f"🔢 البند: {match['hs6_global']}")
else:
    print("❌ لم أستطع تحديد المادة بدقة.")
