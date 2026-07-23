"""
空氣品質分析　Python 鷹架（scaffold）— 時間序列

骨架、函式簽名、流程順序、GATE 都已固定，不要改動結構。
標 # TODO 的地方自己填，每個 TODO 都要看得懂在做什麼。
可用 AI 輔助，但填完要自己驗證數字正確。

對應課程：Day 2 第 5 堂（清洗）＋第 6 堂（分析/視覺化/AI 評論）。
資料來源：環境部空氣品質開放資料（免費）。
  課堂一律讀「已快取的樣本檔」，不在現場打 API、不需金鑰。
品質把關重點：AI 會依趨勢斜率說「空氣品質惡化」，但要看 R² 才能分辨真實趨勢或雜訊。
"""

import numpy as np
import pandas as pd
from scipy.stats import linregress

# ====== 全域設定 ======
CACHED_CSV = "data/aqi_sample.csv"   # 課程 repo 內預放的快取樣本（欄位：site,datetime,pm25,status）
VALUE_COL = "pm25"
TARGET_SITES = ["臺中", "沙鹿", "西屯"]   # 標的可自由更換（只改這裡，下面不動）
MISSING_TOKENS = {"", "NA", "N/A", "-", "x", "設備維護", "無效"}   # 空品資料常見缺值標記


# ====== step 1：讀快取樣本 ======
def load_cached(path=CACHED_CSV):
    df = pd.read_csv(path, dtype=str)        # 先全部當字串讀，避免自動轉型出錯
    # GATE：必要欄位存在
    for col in ("site", "datetime", VALUE_COL):
        assert col in df.columns, f"缺少欄位：{col}"
    return df


# ====== step 2：清洗（時間 + 缺值 + 型別）======
def clean(df):
    # TODO: 把 MISSING_TOKENS 內的值全部換成 NaN（提示：df[VALUE_COL].replace(list(MISSING_TOKENS), np.nan)）
    df[VALUE_COL] = df[VALUE_COL].replace(list(MISSING_TOKENS), np.nan)
    # TODO: 把 datetime 欄轉成 pandas 時間（pd.to_datetime(..., errors="coerce")），存回 df["datetime"]
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    # TODO: 把 VALUE_COL 轉成數值（pd.to_numeric(..., errors="coerce")）
    df[VALUE_COL] = pd.to_numeric(df[VALUE_COL], errors="coerce")
    # TODO: 丟掉 datetime 或 VALUE_COL 為 NaN 的列（下一行已固定依時間排序，不必重複）
    df = df.dropna(subset=["datetime", VALUE_COL])
    df = df.sort_values("datetime").reset_index(drop=True)
    return df


# ====== step 3：品質檢核（GATE）======
def quality_check(df):
    # TODO: assert df[VALUE_COL] 已無 NaN
    # TODO: assert df["datetime"] 為時間型別（pd.api.types.is_datetime64_any_dtype）
    # TODO: assert 每個 TARGET_SITES 在資料中至少有 2 筆（才能算趨勢）
    print("品質檢核通過，總筆數：", len(df))


# ====== step 4：趨勢分析（斜率 + R²）======
def analyze_trend(df, site):
    """回傳 (slope, r2, n)。x 用時間序位、y 用測值。"""
    sub = df[df["site"] == site].sort_values("datetime")
    x = np.arange(len(sub))                       # 以序位代表時間先後
    y = sub[VALUE_COL].to_numpy(dtype=float)
    # TODO: 用 linregress(x, y) 取得斜率與 r 值；R² = r 值平方
    result = linregress(x, y)
    slope = result.slope
    r2 = result.rvalue ** 2
    return slope, r2, len(sub)


# ====== step 5：AI 品質把關（重點教學）======
def verdict(slope, r2):
    """把斜率＋R² 翻成有把握的結論，而不是只看斜率喊「惡化」。"""
    # TODO: 規則：只有當 |slope|>0 且 R²>=0.5 才下「趨勢明顯」的判斷；
    #       R²<0.5 一律回「波動大、趨勢不明顯（疑似雜訊）」。
    #       這就是「AI 生成、教師把關」：AI 看斜率說惡化，你用 R² 擋下雜訊。
    if r2 >= 0.5 and slope > 0:
        return f"趨勢明顯：上升（斜率 {slope:.3f}）"
    if r2 >= 0.5 and slope < 0:
        return f"趨勢明顯：下降（斜率 {slope:.3f}）"
    return "波動大、趨勢不明顯（疑似雜訊）"


# ====== step 6：視覺化 ======
def make_figure(df, outdir="output"):
    import matplotlib.pyplot as plt
    import os

    site_names = {"臺中": "Taichung", "沙鹿": "Shalu", "西屯": "Xitun"}
    plt.figure(figsize=(10, 6))
    for site in TARGET_SITES:
        sub = df[df["site"] == site].sort_values("datetime")
        plt.plot(sub["datetime"], sub[VALUE_COL], label=site_names.get(site, site))

    plt.title("PM2.5 hourly trend, 2026-07-01 to 07-14")
    plt.xlabel("Date")
    plt.ylabel("PM2.5 (ug/m3)")
    plt.ylim(bottom=0)
    plt.legend()
    plt.tight_layout()
    os.makedirs(outdir, exist_ok=True)
    plt.savefig(
        os.path.join(outdir, "aqi_trend.png"),
        dpi=150,
        bbox_inches="tight",
    )
    plt.close()


# ====== 主程式 ======
if __name__ == "__main__":
    import os
    os.makedirs("output", exist_ok=True)

    df = load_cached()
    df = clean(df)
    quality_check(df)                  # GATE

    for site in TARGET_SITES:
        slope, r2, n = analyze_trend(df, site)
        print(f"{site}: slope={slope}, R²={r2}, n={n} → {verdict(slope, r2)}")

    make_figure(df)
    print("完成。請檢查 output 資料夾。")
def quality_check(df):
    # TODO: assert df[VALUE_COL] 已無 NaN
    assert not df[VALUE_COL].isna().any(), f"{VALUE_COL} 欄位仍含有 NaN 或 NaT 值！"

    # TODO: assert df["datetime"] 為時間型別（pd.api.types.is_datetime64_any_dtype）
    assert pd.api.types.is_datetime64_any_dtype(df["datetime"]), "datetime 欄位型態並非 Pandas datetime 型態！"

    # TODO: assert 每個 TARGET_SITES 在資料中至少有 2 筆（才能算趨勢）
    assert (df["site"].value_counts().reindex(TARGET_SITES, fill_value=0) >= 2).all(), "部分 TARGET_SITES 測站資料筆數少於 2 筆！"

    print("品質檢核通過，總筆數：", len(df))

💡 關鍵實作細節說明：

    not df[VALUE_COL].isna().any()

        .isna().any() 會檢查欄位中是否有任何一個 NaN/None。加上 not 確保「完全沒有 NaN」時才通過斷言。

    pd.api.types.is_datetime64_any_dtype(df["datetime"])

        這是 Pandas 官方推薦的純粹型別檢查方式，可完美相容各種時區設定或不同精度的 datetime64 類型。

    df["site"].value_counts().reindex(TARGET_SITES, fill_value=0) >= 2

        使用 .reindex(TARGET_SITES, fill_value=0) 的好處是：如果某個指定站點在清洗後完全被刪光（0 筆），value_counts() 本身是不會列出該站點的；透過 reindex 補 0 可以防止遺漏未出現的站點，確保每一站都妥善被檢查到。def verdict(slope, r2):
    """把斜率＋R² 翻成有把握的結論，而不是只看斜率喊『惡化』。"""
    if r2 >= 0.5 and slope > 0:
        return f"趨勢明顯：上升（斜率 {slope:.3f}）"
    if r2 >= 0.5 and slope < 0:
        return f"趨勢明顯：下降（斜率 {slope:.3f}）"
    return "波動大、趨勢不明顯（疑似雜訊）"
