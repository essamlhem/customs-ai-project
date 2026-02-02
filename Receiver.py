import json
from difflib import SequenceMatcher, get_close_matches

# قاموس المصطلحات العامية
SYRIAN_SYNONYMS = {
    "دواليب": "إطارات مطاطية",
    "كمبريسة": "ضاغط هواء",
    "موتورات": "محرك احتراق داخلي",
    "جنطات": "إطارات معدنية",
    "نبريش": "أنابيب وخراطيم",
    "لدات": "صمامات ثنائية باعثة للضوء",
    "بطاريات جيل": "مدخرات كهربائية",
    "راوتر": "أجهزة إرسال واستقبال بيانات",
    "مكيفات": "أجهزة تكييف هواء",
    "قماش": "منسوجات"
}

def clean_input(user_query):
    query = user_query.strip().lower()
    words = query.split()
    translated_words = [SYRIAN_SYNONYMS.get(w, w) for w in words]
    return " ".join(translated_words)

def calculate_confidence(str1, str2):
    return round(SequenceMatcher(None, str1, str2).ratio() * 100, 1)

def find_best_match_with_score(query, database_path="knowledge_base.json"):
    try:
        with open(database_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        materials_list = [item['material_clean'] for item in data]
        matches = get_close_matches(query, materials_list, n=1, cutoff=0.2)
        
        if matches:
            match_name = matches[0]
            confidence = calculate_confidence(query, match_name)
            result = next(item for item in data if item['material_clean'] == match_name)
            result['confidence_score'] = confidence
            return result
        return None
    except Exception as e:
        print(f"Error in find_best_match: {e}")
        return None
