import json
from difflib import SequenceMatcher, get_close_matches

# ... (نفس قاموس المرادفات السابق) ...

def calculate_confidence(str1, str2):
    """حساب نسبة التشابه بين كلمتين"""
    return round(SequenceMatcher(None, str1, str2).ratio() * 100, 1)

def find_best_match_with_score(query, database_path="knowledge_base.json"):
    try:
        with open(database_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        materials_list = [item['material_clean'] for item in data]
        
        # الحصول على أفضل تطابق
        matches = get_close_matches(query, materials_list, n=1, cutoff=0.2)
        
        if matches:
            match_name = matches[0]
            confidence = calculate_confidence(query, match_name)
            
            # جلب البيانات الكاملة
            result = next(item for item in data if item['material_clean'] == match_name)
            
            # إضافة نسبة الدقة للنتيجة
            result['confidence_score'] = confidence
            return result
        return None
    except Exception as e:
        return f"Error: {e}"

# --- تجربة التشغيل ---
user_ask = "بدي جيب بطيخ" # تجربة كلمة غير موجودة بدقة
processed = clean_input(user_ask)
match = find_best_match_with_score(processed)

if match:
    # إذا كانت الدقة أقل من 60%، ننبه المستخدم
    status = "✅ مؤكد" if match['confidence_score'] > 75 else "⚠️ تقريبي"
    print(f"الحالة: {status} ({match['confidence_score']}%)")
    print(f"المنتج: {match['material_clean']}")
else:
    print("❌ الدقة 0% - المادة غير موجودة")
