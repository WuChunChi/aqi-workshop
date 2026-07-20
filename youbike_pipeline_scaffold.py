"""
YouBike 分析　Python 鷹架（scaffold）— 橫斷面

對應課程：Day 2 第 7 堂，在空品範本上「換資料來源」，改成 YouBike。
重點：同一套管線骨架（讀取→清洗→分析→視覺化），但資料型態從「時間序列」變「橫斷面」，
      分析從「趨勢」變「跨站點/跨行政區比較」。

資料來源：各縣市 YouBike 開放資料（免費、多數不需金鑰）。
  課堂一律讀「已快取的樣本檔」，不在現場打 API。
"""

import numpy as np
import pandas as pd

# ====== 全域設定 ======
CACHED_CSV = "data/youbike_sample.csv"   # repo 內快取（sno,sna,sarea,tot,sbi,bemp,lat,lng）


# ====== step 1：讀快取樣本 ======
def load_cached(path=CACHED_CSV):
    df = pd.read_csv(path, dtype=str)
    for col in ("sna", "sarea", "tot", "sbi"):
        assert col in df.columns, f"缺少欄位：{col}"
    return df


# ====== step 2：清洗（型別 + 除零防護）======
def clean(df):
    # TODO: 把 tot、sbi 轉成數值（pd.to_numeric(..., errors="coerce")）
    # TODO: 丟掉 tot 或 sbi 為 NaN 的列
    # TODO: 丟掉 tot <= 0 的站（沒有車架，算可借率會除以零）
    return df


# ====== step 3：品質檢核（GATE）======
def quality_check(df):
    # TODO: assert df["tot"] 全部 > 0
    # TODO: assert df["sbi"] 全部 >= 0 且 <= df["tot"]（可借不可能超過總數）
    print("品質檢核通過，站點數：", len(df))


# ====== step 4：橫斷面分析（可借率 + 依行政區比較）======
def analyze(df):
    # TODO: 新增一欄 df["avail_rate"] = sbi / tot（可借率，0~1）
    # TODO: by_area = 依 sarea 分組算可借率平均（groupby("sarea")["avail_rate"].mean()）
    # TODO: 找出可借率最高與最低的站（df.sort_values("avail_rate")）
    by_area = None
    print(by_area)
    return by_area


# ====== step 5：視覺化 ======
def make_figure(df, by_area, outdir="output"):
    import matplotlib.pyplot as plt
    # TODO: 以長條圖呈現各行政區平均可借率（by_area）
    # TODO:（進階）用經緯度 lat/lng 畫散點地圖，顏色對應可借率
    # TODO: 存成 output/youbike_avail.png
    pass


# ====== 主程式 ======
if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)

    df = load_cached()
    df = clean(df)
    quality_check(df)              # GATE
    by_area = analyze(df)
    make_figure(df, by_area)
    print("完成。請檢查 output 資料夾。")
