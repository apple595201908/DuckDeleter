import os
import sys
import shutil

sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = r"c:\Users\user\Desktop\MonsterDeleter"
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
AUDIO_DIR = os.path.join(ASSETS_DIR, "音频")
BG_DIR = os.path.join(ASSETS_DIR, "选择界面")

def organize():
    print("Organizing DuckDeleter project structure...")

    # 1. Standardize Audio names with full compatibility
    audio_mappings = [
        ("怪兽说话.mp3", "duck_quack.mp3"),
        ("bgm(1).mp3", "duck_bgm.mp3"),
        ("爆炸.mp3", "duck_pop.mp3")
    ]
    for old_name, new_name in audio_mappings:
        old_path = os.path.join(AUDIO_DIR, old_name)
        new_path = os.path.join(AUDIO_DIR, new_name)
        if os.path.exists(old_path) and not os.path.exists(new_path):
            shutil.copy2(old_path, new_path)
            print(f"Created audio alias: {new_name}")

    # 2. Standardize Spritesheet names with full compatibility
    sprite_mappings = [
        ("走路动效_spritesheet_transparent.png", "duck_walk_spritesheet.png"),
        ("指着文件_spritesheet_transparent.png", "duck_point_spritesheet.png"),
        ("踹文件动效_spritesheet_transparent.png", "duck_kick_spritesheet.png"),
        ("爆炸_spritesheet_transparent.png", "duck_pop_spritesheet.png"),
        ("雷欧登场_spritesheet_transparent.png", "duck_victory_spritesheet.png"),
        ("出场飞行动效_spritesheet_transparent.png", "duck_fly_spritesheet.png")
    ]
    for old_name, new_name in sprite_mappings:
        old_path = os.path.join(ASSETS_DIR, old_name)
        new_path = os.path.join(ASSETS_DIR, new_name)
        if os.path.exists(old_path) and not os.path.exists(new_path):
            shutil.copy2(old_path, new_path)
            print(f"Created sprite alias: {new_name}")

    # 3. Clean up obsolete monster legacy test scripts in tests/
    old_test_files = [
        "mouse_tracker.py",
        "test_dump.py",
        "test_find_item.py",
        "test_point.py",
        "test_selection.py",
        "test_uiauto.py"
    ]
    for f in old_test_files:
        p = os.path.join(ROOT_DIR, "tests", f)
        if os.path.exists(p):
            os.remove(p)
            print(f"Removed legacy test script: {f}")

    # 4. Clean up obsolete monster scripts in scripts/
    old_scripts = [
        "batch_bg_remove.py",
        "batch_rembg.py",
        "batch_rembg_slice.py",
        "process_image.py"
    ]
    for f in old_scripts:
        p = os.path.join(ROOT_DIR, "scripts", f)
        if os.path.exists(p):
            os.remove(p)
            print(f"Removed legacy script: {f}")

    print("Project directory organized cleanly!")

if __name__ == "__main__":
    organize()
