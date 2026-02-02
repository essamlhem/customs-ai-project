from Receiver import find_best_match_semantic

class AcrossMenaBrain:
    def __init__(self):
        self.db_path = "knowledge_base.json"

    def ask(self, user_query):
        # البحث بالمعنى
        match = find_best_match_semantic(user_query, self.db_path)

        # إذا كانت الدقة ضعيفة جداً (أقل من 20)
        if not match or match['confidence_score'] < 20:
            return f"❌ عذراً يا عيسى، مادة '{user_query}' غير موجودة حالياً. جرب بكلمات أخرى."

        name = match.get('material_clean', 'غير معروف')
        hs_code = match.get('hs6_global', '000000')
        price = match.get('priceFull', 'غير متوفر')
        confidence = match.get('confidence_score', 0)
        
        return (f"🎯 Across MENA AI:\n"
                f"-------------------\n"
                f"📦 المنتج: {name}\n"
                f"🔢 البند: {hs_code}\n"
                f"💰 السعر: {price}\n"
                f"📊 الدقة: {confidence}%\n"
                f"-------------------")
