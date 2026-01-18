import requests
import pandas as pd
import os
import time

# 台北市停車場即時資料真實網址
URL = "https://tcgbusfs.blob.core.windows.net/blobtcmsv/TCMSV_allavailable.json"
CSV_FILE = "parking_data.csv"

def scrape_data():
    try:
        print("🚀 啟動爬蟲...")
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        # 取得資料時間
        update_time = data['data']['UPDATETIME']
        parks = data['data']['park']
        print(f"資料時間點: {update_time}")

        # 轉成 DataFrame
        df = pd.DataFrame(parks)
        
        # 只保留關鍵欄位
        cols = ['id', 'availablecar', 'availablemotor']
        df = df[cols]
        df['update_time'] = update_time

        # 存檔邏輯 (自動判斷是新增還是附加)
        if os.path.exists(CSV_FILE):
            # 檔案存在 -> 附加模式 (append)，不寫入欄位名稱
            df.to_csv(CSV_FILE, mode='a', header=False, index=False, encoding='utf-8')
            print(f"✅ 資料已附加到 {CSV_FILE}")
        else:
            # 檔案不存在 -> 寫入模式 (write)，寫入欄位名稱
            df.to_csv(CSV_FILE, mode='w', header=True, index=False, encoding='utf-8')
            print(f"✅ 已建立新檔案 {CSV_FILE}")

    except Exception as e:
        print(f"❌ 發生錯誤: {e}")
        exit(1)

if __name__ == "__main__":
    scrape_data()
