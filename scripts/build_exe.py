import os
import sys
import shutil
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\user\Desktop\MonsterDeleter"
PROJECT_16_DIR = r"C:\Users\user\Documents\Codex\2026-08-08\new-chat\outputs\vue-core-annotated\專案分類整理_Projects\16_可愛插畫鴨鴨檔案刪除助手_Desktop_Duck_Deleter"

def build():
    print("Building DuckDeleter.exe with PyInstaller...")
    cmd = [
        os.path.join(ROOT_DIR, ".venv", "Scripts", "pyinstaller.exe"),
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name", "DuckDeleter",
        "--add-data", "assets;assets",
        "--hidden-import", "send2trash",
        "--hidden-import", "comtypes",
        "--hidden-import", "uiautomation",
        os.path.join(ROOT_DIR, "main.py")
    ]
    subprocess.run(cmd, check=True, cwd=ROOT_DIR)
    
    exe_src = os.path.join(ROOT_DIR, "dist", "DuckDeleter.exe")
    if os.path.exists(exe_src):
        # 1. Copy to workspace root
        shutil.copy2(exe_src, os.path.join(ROOT_DIR, "DuckDeleter.exe"))
        print(f"Copied to {os.path.join(ROOT_DIR, 'DuckDeleter.exe')}")
        
        # 2. Copy to Project 16 Hub
        if os.path.exists(PROJECT_16_DIR):
            os.makedirs(os.path.join(PROJECT_16_DIR, "dist"), exist_ok=True)
            shutil.copy2(exe_src, os.path.join(PROJECT_16_DIR, "dist", "DuckDeleter.exe"))
            shutil.copy2(exe_src, os.path.join(PROJECT_16_DIR, "DuckDeleter.exe"))
            print(f"Synchronized to Project 16: {PROJECT_16_DIR}")
            
    print("Build and distribution finished successfully!")

if __name__ == "__main__":
    build()
