import pandas as pd

# 1. 讀取尚未填寫地質代碼的特徵表
try:
    df = pd.read_csv("station_geology.csv")
    print("成功讀取 station_geology.csv！開始填寫地質代碼...")
except FileNotFoundError:
    print("找不到 station_geology.csv，請確認檔案在同一個資料夾。")
    exit()

# 2. 建立 AI 預建的測站地質分類字典 (Geology_Code)
# 這是根據台灣地質圖與各 BATS 測站位置所建立的分類
geology_dict = {
    # Code 1: 堅硬岩盤 (變質岩、火成岩)
    'NACB': 1, 'TDCB': 1, 'WARB': 1, 'PHUB': 1, 'FUSB': 1, 
    'NNSB': 1, 'HOPB': 1, 'LXI1': 1, 'MATB': 1, 'VNAS': 1, 
    'LYUB': 1, 'KMNB': 1, 'GWUB': 1, 'WUSB': 1, 'TPUB': 1,
    
    # Code 2: 中等硬度 (礫石台地、古老沉積岩)
    'VDOS': 2, 'LATB': 2, 'SBCB': 2, 'SYNB': 2, 'MASB': 2, 
    'YD07': 2, 'WFSB': 2,
    
    # Code 3: 鬆軟土層 (全新世沖積層、盆地)
    'VWUC': 3, 'HWLB': 3, 'TWGB': 3, 'TUIB': 3, 'RLNB': 3, 
    'YHNB': 3, 'HGSD': 3, 'VCHM': 3, 'SSLB': 3, 'YULB': 3
}

# 3. 定義一個函數來進行配對
def get_geology_code(station_name):
    # 如果字典裡有這個測站，就回傳代碼；如果沒有，預設給 2 (中等硬度)
    return geology_dict.get(station_name, 2)

# 4. 執行填寫
df['Geology_Code'] = df['Station'].apply(get_geology_code)

# 5. 存檔並輸出結果
df.to_csv("station_geology_final.csv", index=False)

print("\n大功告成！所有測站的地質代碼已自動填寫完畢。")
print("檔案已另存為: station_geology_final.csv")
print("\n預覽前幾筆資料：")
print(df[['Station', 'Distance_km', 'Elevation_m', 'Geology_Code']].head(10))