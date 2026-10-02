import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score

# 1. 讀取最終版的特徵與目標值資料表
try:
    df = pd.read_csv("station_geology_final.csv")
except FileNotFoundError:
    print("找不到 station_geology_final.csv 檔案！請確認檔名與路徑。")
    exit()

# 由於先前的 API 呼叫可能會讓少數測站的高程為 NaN (空值)
# 機器學習模型不接受空值，所以我們將有缺漏資料的列直接刪除
df_clean = df.dropna(subset=['Elevation_m', 'Distance_km', 'Geology_Code', 'Max_Amplification'])
print(f"清理空值後，共使用 {len(df_clean)} 筆有效測站資料進行訓練。\n")

# 2. 定義輸入特徵 (X) 與預測目標 (Y)
X = df_clean[['Elevation_m', 'Distance_km', 'Geology_Code']]
y = df_clean['Max_Amplification']

# 3. 切割訓練集與測試集 (80% 用於訓練 AI，20% 用於像考試一樣測試準確度)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 4. 建立與訓練隨機森林迴歸模型
# n_estimators=100 代表我們在森林裡種了 100 棵決策樹來共同投票預測
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# 5. 模型預測與評估
y_pred = rf_model.predict(X_test)
r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)

print("========== 訓練結果 ==========")
print(f"決策係數 (R2 Score): {r2:.3f} (滿分 1.0，越高代表預測越準確)")
print(f"均方誤差 (MSE): {mse:.3f} (數值越低越好)")

# 6. 特徵重要性分析
# 讓 AI 告訴我們，它覺得哪一個因素對震度放大的影響最大
importances = pd.Series(rf_model.feature_importances_, index=X.columns)
print("\n========== 特徵重要性排名 ==========")
print(importances.sort_values(ascending=False).to_string())