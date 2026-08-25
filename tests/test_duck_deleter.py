import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QImage, QPixmap

# Ensure offscreen platform for headless test if needed
os.environ["QT_QPA_PLATFORM"] = "windows"

class TestDuckDeleter(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def test_asset_loading(self):
        from main import SPRITE_DIR, SpriteAnimator
        
        animations = [
            "走路动效_spritesheet.png",
            "指着文件_spritesheet.png",
            "踹文件动效_spritesheet.png",
            "爆炸_spritesheet.png",
            "雷欧登场_spritesheet.png",
            "出场飞行动效_spritesheet.png"
        ]
        
        animator = SpriteAnimator()
        for anim_name in animations:
            path = os.path.join(SPRITE_DIR, anim_name)
            success = animator.load_spritesheet(path, cols=5, rows=3, target_height=240)
            self.assertTrue(success, f"Failed to load spritesheet: {anim_name}")
            self.assertEqual(len(animator.frames), 15, f"{anim_name} did not have 15 frames")
            print(f"Verified {anim_name}: {len(animator.frames)} frames, frame size: {animator.frames[0].size().width()}x{animator.frames[0].size().height()}")

    def test_ui_creation(self):
        from main import DuckDeleter, BubbleWidget, ChoicesWidget
        
        bubble = BubbleWidget("測試對話")
        self.assertIsNotNone(bubble)
        
        choices = ChoicesWidget()
        self.assertIsNotNone(choices)
        
        deleter = DuckDeleter(target_file=None)
        self.assertIsNotNone(deleter)
        print("Verified DuckDeleter, BubbleWidget, and ChoicesWidget initialization successfully.")

if __name__ == "__main__":
    unittest.main()
