import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.stdout.reconfigure(encoding='utf-8')

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt, QPoint
from main import DuckDeleter

class TestDuckSequence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication(sys.argv)

    def test_full_sequence_transitions(self):
        deleter = DuckDeleter(target_file=None)
        deleter.show()
        deleter.target_pos = QPoint(500, 500)
        
        # Test Phase 1 -> Phase 2
        deleter.start_phase1_walk()
        self.assertTrue(deleter.animator.isVisible())
        
        # Test Phase 2 Pointing
        deleter.start_phase2_point()
        self.assertTrue(deleter.animator.isVisible())
        
        # Test Dialog pop up
        deleter.show_dialog()
        self.assertTrue(deleter.bubble.isVisible())
        self.assertTrue(deleter.choices.isVisible())
        
        # Test Phase 3 Kick & Explosion
        deleter.start_phase3_kick()
        deleter.on_kick_frame(5) # Trigger explosion
        self.assertTrue(deleter.explosion_animator.isVisible())
        
        # Test Phase 4 Victory
        deleter.start_phase4_victory()
        self.assertTrue(deleter.animator.isVisible())
        
        # Test Phase 5 Fly
        deleter.start_phase5_fly()
        self.assertTrue(deleter.animator.isVisible())
        
        print("All sequence phases transition smoothly without error!")

if __name__ == "__main__":
    unittest.main()
