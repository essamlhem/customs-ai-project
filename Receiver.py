import json
import numpy as np
from sentence_transformers import SentenceTransformer, util

# تحميل مودل ذكي جداً يفهم اللغة العربية (مجاني ومفتوح المصدر)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def find_best_match_semantic(user_query, database_path="knowledge_base.json"):
    try:
        with open(database_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        materials_list = [item['material_clean'] for item in data]
        
        # تحويل النصوص لمتجهات تفهم المعنى
        query_embedding = model.encode(user_query, convert_to_tensor=True)
        materials_embeddings = model.encode(materials_list, convert_to_tensor=True)
        
        # حساب التشابه المعنوي
        cosine_scores = util.cos_sim(query_embedding, materials_embeddings)[0]
        best_idx = np.argmax(cosine_scores.cpu().numpy())
        
        result = data[best_idx]
        result['confidence_score'] = round(float(cosine_scores[best_idx]) * 100, 1)
        return result
    except:
        return None
