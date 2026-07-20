# 空品資料分析實作（AI 教學實戰營 · Day 2）

用 Git 做版本控制、用 AI 助理（GitHub Copilot ＋ Gemini Code Assist）完成環境部空品資料的清洗與分析。
本 repo 是第 5–7 堂的**單一真實來源**：課堂上 **Fork 本 repo**，在自己的副本開 Codespace、填空、commit。

> 核心句：**AI 負責生成，教師負責把關。**

## 檔案地圖

| 檔案 | 用途 | 對應堂次 |
|---|---|---|
| `air_quality_pipeline_scaffold.py` | 空品管線鷹架（骨架固定，填 `# TODO`） | 第 5 堂（清洗）＋第 6 堂（分析／視覺化） |
| `data/aqi_sample.csv` | 已快取的空品樣本（3 站 × 14 天小時值，含真實常見的髒點） | 第 5–6 堂 |
| `youbike_pipeline_scaffold.py` | YouBike 橫斷面鷹架（同一套骨架、換資料） | 第 7 堂 |
| `data/youbike_sample.csv` | 已快取的 YouBike 快照（臺中 120 站 × 8 行政區，含髒點） | 第 7 堂 |
| `requirements.txt` | Python 套件清單（環境建立時自動安裝） | — |
| `.devcontainer/` | 共用雲端環境設定（一條連結、免安裝） | — |

## 三條規則

1. **骨架不動，只填 TODO**——函式簽名、流程順序、GATE 都已固定。
2. **GATE 沒過就不往下**——`quality_check()` 印出「品質檢核通過」才算完成清洗。
3. **每完成一段就 commit**——commit 訊息記錄「AI 建議了什麼、你改了什麼、為什麼」。

## 資料說明

`data/aqi_sample.csv` 為課堂快取樣本（欄位：`site,datetime,pm25,status`），
髒點型態與環境部開放資料實務相符：缺值標記（空白、`NA`、`N/A`、`-`、`x`、`設備維護`、`無效`）與少量無法解析的時間值。
兩份樣本皆為**固定種子產生的教學用合成資料**（統計性質仿真、髒點刻意設計），非官方觀測值。
正式資料來源：環境部環境資料開放平臺（data.moenv.gov.tw），課堂不現場打 API。

## 參與學員

> 第 5 堂任務 2：在下方加上你的姓名與系所，完成第一次 commit。

- 胡維桓（醫學資訊學系，示範）
