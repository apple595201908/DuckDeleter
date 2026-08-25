# 🦆 可愛插畫鴨鴨檔案刪除助手 - Desktop Duck Deleter

<p align="center">
  <a href="https://github.com/apple595201908/DuckDeleter/raw/main/DuckDeleter_Setup_v1.0.0.exe">
    <img src="https://img.shields.io/badge/⬇️_一鍵下載-Windows_完整安裝包_(.exe)-ff9900?style=for-the-badge&logo=windows&logoColor=white" alt="下載安裝包">
  </a>
</p>

> 💡 **快速下載連結**：[👉 點此直接下載 DuckDeleter_Setup_v1.0.0.exe](https://github.com/apple595201908/DuckDeleter/raw/main/DuckDeleter_Setup_v1.0.0.exe)

---

## ✨ 核心亮點

- 🚀 **極速右鍵直接吃掉（無須準心瞄準）**：
  - 安裝完成後，直接在任何檔案或資料夾「按滑鼠右鍵」點擊 **「召喚可愛鴨鴨吃掉 🦆」**。
  - 小黃鴨會立即邁著小橘腳飛撲走到目標檔案前，確認後大口咬下吞掉！
- 🦆 **超萌鴨鴨全套逐幀動效**：
  - 🚶 **搖擺走路**：小黃鴨搖頭擺尾走入螢幕。
  - 👆 **歪頭指認**：歪頭指著檔案詢問確認「呱？要把這個檔案大口吃掉嗎？😋✨」。
  - 👄 **張開大嘴吃掉**：超搞笑又可愛的**張開巨大圓嘴**飛撲咬下檔案、鼓起腮幫子開心咀嚼 (Nom Nom Nom)、滿足吞下並舔嘴巴！
  - 💥 **Q 彈羽毛爆破**：漫天飄落的軟綿綿小鴨羽毛、閃亮黃金星星與愛心爆破。
  - 😎 **墨鏡勝利 Pose**：小黃鴨戴上帥氣迷你黑墨鏡、摸摸圓滾滾小肚肚。
  - 🚁 **螺旋槳起飛**：頭戴旋轉竹蜻蜓螺旋槳帽，拍動翅膀歡樂飛出螢幕。
- 🎵 **超可愛專屬鴨鴨音效與配樂**：
  - 🐥 **鴨鴨對話萌音**：清脆可愛的「呱呱～！嘎嘎～！✨」鴨鴨語音。
  - 😋 **大口吃掉咀嚼音**：卡哇伊卡通咬下 (CHOMP!)、嚼嚼嚼 (Nom Nom Nom) 與滿足咕嚕吞下 (Gulp!) 音效。
  - 💥 **Q 彈魔法爆破音**：漫畫風「啵！(BOING-POP!)」彈跳與漫天閃亮星光音效。
  - 🎶 **歡樂小黃鴨進行曲 BGM**：木琴 (Marimba) 與輕快撥弦結合的歡樂治癒背景音樂。
- 📦 **專屬 Windows 安裝引導包 (Setup Installer)**：
  - 執行 `DuckDeleter_Setup_v1.0.0.exe` 自動完成安裝。
  - 自動註冊右鍵選單、桌面與開始功能表捷徑，附帶完整解除安裝支援。

---

## 📦 如何使用

### 1. 安裝程式
- 執行 **`DuckDeleter_Setup_v1.0.0.exe`**，依指示點擊下一步完成安裝。

### 2. 右鍵直接吃掉檔案
- 在桌面或任意資料夾中，在任何檔案或資料夾上點擊 **滑鼠右鍵**。
- 選擇 **「召喚可愛鴨鴨吃掉 🦆」**。
- 小黃鴨便會自動跑過來吃掉檔案！

> ⚠️ **安全提醒**：程式使用 `send2trash`（安全移至 Windows 資源回收筒）而非永久粉碎，如果不小心手滑，隨時可以從資源回收筒輕鬆還原。

---

## 🛠️ 開發與建置 (Developer Guide)

### 1. 安裝依賴
```bash
pip install -r requirements.txt
```

### 2. 本地執行測試
```bash
# 開啟啟動助手
python main.py

# 指定檔案直接吃掉
python main.py "C:\path\to\your\file.txt"
```

### 3. 一鍵打包執行檔與 Inno Setup 安裝包
```bash
# 1. 編譯 PyInstaller 執行檔
python scripts\build_exe.py

# 2. 編譯 Windows Setup 安裝包
iscc DuckDeleter_Setup.iss
```

---

## 📂 專案結構
```
MonsterDeleter/
│
├── main.py                     # 核心主程式 (動畫排程、直接右鍵模式、啟動器介面)
├── DuckDeleter_Setup.iss        # Inno Setup 專屬安裝包腳本
├── DuckDeleter_Setup_v1.0.0.exe # Windows 完整安裝導引程式 (Setup)
├── requirements.txt            # Python 依賴清單
├── assets/                     # 美術圖標與音訊資源
│   ├── app_icon.ico            # 專屬高解析小鴨應用程式圖標
│   ├── 音频/                   # BGM、鴨叫、咀嚼、爆炸音效
│   └── *_spritesheet.png       # 鴨鴨全系列透明動態序列幀
└── scripts/                    # 打包與自動化腳本
```
