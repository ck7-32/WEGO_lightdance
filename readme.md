# WEGO_lightdance | 薇閣光舞機電研究社

本專案為結合【光效編排 + LED 控制】的跨平台系統，透過圖形化介面編輯燈光動畫，並傳送指令至 ESP32 控制器，驅動實體服裝燈條同步演出。

## 🔧 系統架構總覽

本系統分為三個主要模組：

### 1. 編輯端（Editor）
- **介面技術**：Python + PyQt6 + QWebEngine（整合 HTML 前端動畫模擬器simulator）
- **功能**：
  - 編輯每幀燈光動畫
  - 編輯舞者走位
  - 以時間軸與標籤方式方便編輯
  - 撥放預覽時同時UDP廣播 操控硬體
  - 可模擬 LED 效果畫面

### 2. 傳輸端（Firebase or Local）
- **Firebase 同步**：將燈光資料上傳至雲端，供多裝置接收
- **本地模式**：也可匯出 JSON，透過 USB / WiFi 傳送

### 3. 舞者端（ESP32）
- **硬體**：ESP32 + WS2812B LED 燈條
- **通訊**：
  - UDP 廣播接收控制訊號（多裝置同步）
  - 依據 Firebase JSON 資料解析燈光動畫
- **軟體語言**：Arduino C++（使用 FastLED  函式庫 控制）

## 📌 系統示意圖

> 下圖完整呈現系統資料流與程式之間的分工：

![image](https://hackmd.io/_uploads/H1uTBh5uC.png)

---

## 🧪 技術特點與設計亮點

- **圖形化時間軸編輯器**：不需寫程式即可編排多軌燈光動畫  
- **多舞者控制架構**：每位舞者皆具獨立編輯通道，支援分區燈條  
- **支援 Layer 疊加、複製貼上、滑鼠編輯**：操作直覺、效率高  
- **支援模擬器與實體同步預覽**：調整動作與燈效更加便利  
- **UDP 廣播設計**：可大規模同步多台 ESP32 控制器  
- **實體 ESP32 韌體穩定性強**：支援 JSON 快取與音樂對拍

---

## 🖥️ 開發與執行環境

### 1. 安裝套件
```bash
pip install PyQt6 PyQt6-WebEngine
```
### 2. 執行編輯器
```bash
python editor.py
```
## 📄 文件與延伸閱讀
HackMD 教學文件（包含環境設置、ESP32 燒錄、使用教學等）
👉 https://hackmd.io/@Wego-lightdance/HkHj0pHFC

## 🤝 開發與維護
由 薇閣光舞機電研究社 開發