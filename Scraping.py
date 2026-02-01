import requests
import pandas as pd
import re

# الإعدادات الأصلية
api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"
headers = {
    'apikey': api_key.strip(),
    'Authorization': f'Bearer {api_key.strip()}',
    'Content-Type': 'application/json'
}

def clean_and_process():
    try:
        # 1. سحب البيانات
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            
            # 2. حذف عمود band القديم
            if 'band' in df.columns:
                df.drop(columns=['band'], inplace=True)

            # 3. دالة استخراج الرقم (البند) من النص
            def extract_band(text):
                if pd.isna(text): return ""
                match = re.search(r'\d+', str(text)) # يبحث عن أول سلسلة أرقام
                return match.group() if match else ""

            # 4. إنشاء عمود band الجديد واستخراج الرقم فيه
            df['band'] = df['material'].apply(extract_band)

            # 5. تنظيف عمود material (حذف الأرقام والرموز الزائدة)
            df['material'] = df['material'].str.replace(r'\d+', '', regex=True) # حذف الأرقام
            df['material'] = df['material'].str.replace(r'[^\w\s]', '', regex=True) # حذف الرموز
            df['material'] = df['material'].str.strip() # حذف المسافات الزائدة

            # 6. إعادة ترتيب الأعمدة (البند أولاً ثم الوصف ثم الباقي)
            cols = ['band', 'material'] + [c for c in df.columns if c not in ['band', 'material']]
            df = df[cols]

            # 7. حفظ الملف المنسق
            df.to_excel("customs_full_data.xlsx", index=False)
            print(f"✅ Success: Data cleaned and saved at {pd.Timestamp.now()}")
        else:
            print(f"❌ API Error: {response.status_code}")
            
    except Exception as e:
        print(f"⚠️ Error occurred: {e}")

if __name__ == "__main__":
    clean_and_process()
