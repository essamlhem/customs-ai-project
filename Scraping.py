import requests
import pandas as pd
import os

# الإعدادات من ملفك الأصلي
api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

headers = {
    'apikey': api_key.strip(),
    'Authorization': f'Bearer {api_key.strip()}',
    'Content-Type': 'application/json'
}

def run_scraping():
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            # حفظ الملف في المجلد الحالي
            df.to_excel("customs_full_data.xlsx", index=False)
            print(f"✅ Success: Extracted {len(df)} records.")
        else:
            print(f"❌ Error {response.status_code}")
    except Exception as e:
        print(f"⚠️ Exception: {e}")

if __name__ == "__main__":
    run_scraping()