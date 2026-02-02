import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def find_best_match_semantic(user_query, database_path="knowledge_base.json"):
    try:
        with open(database_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        materials_list = [item['material_clean'] for item in data]
        
        # دمج استفسار المستخدم مع القائمة لتحليلها
        all_texts = materials_list + [user_query]
        
        vectorizer = TfidfVectorizer().fit_transform(all_texts)
        vectors = vectorizer.toarray()
        
        # حساب التشابه بين آخر عنصر (السؤال) وكل العناصر اللي قبله
        cosine_matrix = cosine_similarity([vectors[-1]], vectors[:-1])
        best_idx = cosine_matrix.argmax()
        highest_score = cosine_matrix[0][best_idx] * 100
        
        result = data[best_idx]
        result['confidence_score'] = round(highest_score, 1)
        return result
    except Exception as e:
        print(f"Error: {e}")
        return None
