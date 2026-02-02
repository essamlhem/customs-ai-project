from Receiver import find_best_match_semantic

class AcrossMenaBrain:
    def __init__(self):
        self.db_path = "knowledge_base.json"

    def ask(self, user_query):
        match = find_best_match_semantic(user_query, self.db_path)

        if not match or match['confidence_score'] < 45: 
            return f"❌ عذراً يا عيسى، مادة '{user_query}' غير موجودة في بياناتي الجمركية حالياً."

        return (f"🎯 نتيجة ذكية لـ Across MENA:\n\n"
                f"📦 المنتج: {match['material_clean']}\n"
                f"🔢 البند: {match['hs6_global']}\n"
                f"💰 السعر: {match.get('priceFull', 'غير متوفر')}\n"
                f"📊 الثقة: {match['confidence_score']}%")
