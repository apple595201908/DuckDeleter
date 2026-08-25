import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

hub_path = r"C:\Users\user\Documents\Codex\2026-08-08\new-chat\outputs\vue-core-annotated\專案分類整理_Projects\專案導航入口_Projects_Hub.html"
readme_path = r"C:\Users\user\Documents\Codex\2026-08-08\new-chat\outputs\vue-core-annotated\專案分類整理_Projects\README_目錄索引.md"

duck_card = """
      <!-- 16: 可愛插畫鴨鴨檔案刪除助手 (Desktop Duck Deleter) -->
      <div class="card" style="border-color: rgba(245, 158, 11, 0.5); background: linear-gradient(145deg, #1e293b 0%, #2e1d0c 100%);">
        <div>
          <div class="card-top">
            <div class="icon-box" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.4);">🦆</div>
            <div>
              <div class="card-num" style="color: #fbbf24;">WINDOWS DESKTOP APP • 16</div>
              <div class="card-title">可愛插畫鴨鴨檔案刪除助手 (Duck Deleter)</div>
            </div>
          </div>
          <div class="card-desc">
            超治癒 Windows 桌面互動應用！包含 6 組全彩鴨鴨逐幀透明動效（搖擺走路、歪頭指認、飛踢打擊、羽毛星星爆破、墨鏡勝利 Pose、螺旋槳起飛），支援 Windows 右鍵選單「召喚可愛鴨鴨吃掉」與 send2trash 安全回收機制。已封裝為單一免安裝 .exe 執行檔。
          </div>
          <div class="card-tags">
            <span class="tag" style="background: rgba(245, 158, 11, 0.2); color: #fde68a; border-color: rgba(245, 158, 11, 0.3);">🦆 可愛小黃鴨</span>
            <span class="tag" style="background: rgba(59, 130, 246, 0.2); color: #93c5fd; border-color: rgba(59, 130, 246, 0.3);">PyQt6 逐幀動效</span>
            <span class="tag">獨立 .exe 檔</span>
            <span class="tag">Windows 右鍵選單</span>
            <span class="tag">send2trash 安全防護</span>
          </div>
        </div>
        <div class="card-footer">
          <a href="./16_可愛插畫鴨鴨檔案刪除助手_Desktop_Duck_Deleter/dist/DuckDeleter.exe" class="btn-launch" style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: #fff; font-weight: 800;">
            <span>🚀</span> 下載/執行 DuckDeleter.exe
          </a>
          <a href="./16_可愛插畫鴨鴨檔案刪除助手_Desktop_Duck_Deleter/README.md" class="btn-secondary" style="border-color: #fbbf24; color: #fde68a;">
            <span>📖</span> 專案說明
          </a>
          <a href="./16_可愛插畫鴨鴨檔案刪除助手_Desktop_Duck_Deleter/" class="btn-secondary">
            <span>📁</span> 專案目錄
          </a>
        </div>
      </div>
"""

if os.path.exists(hub_path):
    with open(hub_path, 'r', encoding='utf-8') as f:
        hub_content = f.read()
    if '可愛插畫鴨鴨檔案刪除助手' not in hub_content:
        hub_content = hub_content.replace('    </div>\n  </div>\n\n</body>', duck_card + '    </div>\n  </div>\n\n</body>')
        with open(hub_path, 'w', encoding='utf-8') as f:
            f.write(hub_content)
        print('Updated Projects_Hub.html')

duck_readme_sec = """
---

### 📁 16_可愛插畫鴨鴨檔案刪除助手 (Desktop Duck Deleter)
* **路徑**：`專案分類整理_Projects/16_可愛插畫鴨鴨檔案刪除助手_Desktop_Duck_Deleter/`
* **特色**：
  * **超治癒 Windows 桌面互動應用**：告別單調刪除提示，召喚呆萌小黃鴨搖晃走到檔案前，一腳踢爆檔案並化為漫天可愛羽毛與星星。
  * **6 大全彩逐幀透明動畫 (5x3)**：
    * 走路動效 (`走路动效_spritesheet_transparent.png`)
    * 歪頭指認動效 (`指着文件_spritesheet_transparent.png`)
    * 飛踢攻擊動效 (`踹文件动效_spritesheet_transparent.png`)
    * 羽毛星星爆破 (`爆炸_spritesheet_transparent.png`)
    * 墨鏡勝利姿態 (`雷欧登场_spritesheet_transparent.png`)
    * 螺旋槳起飛離開 (`出场飞行动效_spritesheet_transparent.png`)
  * **單一獨立 `.exe` 執行檔**：已完整打包於 `dist/DuckDeleter.exe` (約 58MB)，免安裝 Python 即可直接執行。
  * **Windows 右鍵整合**：自動註冊「召喚可愛鴨鴨吃掉」右鍵選單。
  * **安全防護**：底層使用 `send2trash` 安全移至資源回收筒，隨時可還原。
* **啟動方式**：直接雙擊 [dist/DuckDeleter.exe](./16_可愛插畫鴨鴨檔案刪除助手_Desktop_Duck_Deleter/dist/DuckDeleter.exe) 或執行 `python main.py`。
"""

if os.path.exists(readme_path):
    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()
    if '可愛插畫鴨鴨檔案刪除助手' not in readme_content:
        readme_content += duck_readme_sec
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print('Updated README_目錄索引.md')
