import requests
import pandas as pd
import re
from datetime import datetime

# الإعدادات الأصلية
api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"
headers = {
    'apikey': api_key.strip(),
    'Authorization': f'Bearer {api_key.strip()}',
    'Content-Type': 'application/json'
}

def clean_data():
    try:
        # 1. سحب البيانات الخام
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            
            # 2. حذف عمود band القديم (غير الدقيق)
            if 'band' in df.columns:
                df.drop(columns=['band'], inplace=True)

            # 3. استخراج رقم البند من عمود material
            def get_band_number(text):
                if pd.isna(text): return ""
                match = re.search(r'\d+', str(text)) # البحث عن أول رقم
                return match.group() if match else ""

            df['band'] = df['material'].apply(get_band_number)

            # 4. تنظيف عمود material (إزالة الأرقام والرموز والمسافات الزائدة)
            df['material'] = df['material'].str.replace(r'\d+', '', regex=True) # حذف الأرقام
            df['material'] = df['material'].str.replace(r'[^\w\s]', '', regex=True) # حذف الرموز
            df['material'] = df['material'].str.strip() # إزالة المسافات من الأطراف

            # 5. إضافة عمود لتوقيت التحديث
            df['last_update'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 6. إعادة ترتيب الأعمدة (البند أولاً، ثم الوصف، ثم التوقيت، ثم الباقي)
            main_cols = ['band', 'material', 'last_update']
            remaining_cols = [c for c in df.columns if c not in main_cols]
            df = df[main_cols + remaining_cols]

            # 7. حفظ الملف النهائي
            df.to_excel("customs_full_data.xlsx", index=False)
            print(f"✅ تم السحب والتنظيف بنجاح في {datetime.now()}")
        else:
            print(f"❌ فشل الاتصال: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ خطأ أثناء المعالجة: {e}")

if __name__ == "__main__":
    clean_data()
