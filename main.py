import sys
import os
import winreg
import shutil
import urllib.parse
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGraphicsDropShadowEffect
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QEasingCurve, pyqtSignal, QUrl, pyqtProperty
from PyQt6.QtGui import QPixmap, QPainter, QColor, QTransform, QImage, QPainterPath, QCursor, QPen, QFont, QBrush
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

def get_resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

SPRITE_DIR = get_resource_path("assets")
COLS = 5
ROWS = 3

# Visual Scale Constants - Massive, stunning, impactful duck & effect scale
DUCK_SIZE = 380       # Huge adorable duck character
EXPLOSION_SIZE = 460  # Massive comic pop explosion

def get_asset_file(subfolder, *filenames):
    """Find first existing file candidate within assets subfolder."""
    for fn in filenames:
        p = os.path.join(SPRITE_DIR, subfolder, fn) if subfolder else os.path.join(SPRITE_DIR, fn)
        if os.path.exists(p):
            return p
    return os.path.join(SPRITE_DIR, subfolder, filenames[0]) if subfolder else os.path.join(SPRITE_DIR, filenames[0])

def sanitize_path(path_str):
    """Clean and validate a file path."""
    if not path_str:
        return None
    cleaned = str(path_str).strip(' \t\r\n"\'')
    if not cleaned:
        return None
    try:
        norm = os.path.normpath(os.path.abspath(cleaned))
        if os.path.exists(norm):
            return norm
    except Exception:
        pass
    return None

def find_file_from_explorer_selection():
    """Query open Windows Explorer windows or Desktop for selected items."""
    try:
        import comtypes.client
        shell = comtypes.client.CreateObject("Shell.Application")
        for w in shell.Windows():
            try:
                doc = w.Document
                sel = doc.SelectedItems()
                if sel and sel.Count > 0:
                    item = sel.Item(0)
                    p = sanitize_path(item.Path)
                    if p:
                        return p
            except Exception:
                pass
    except Exception:
        pass
    return None

def resolve_file_at_point(x, y):
    """Find target file on Desktop or in Explorer near screen coordinates (x, y)."""
    selected = find_file_from_explorer_selection()
    if selected:
        return selected

    try:
        import uiautomation as auto
        control = auto.ControlFromPoint(x, y)
        curr = control
        item_name = None
        while curr:
            if curr.ControlTypeName in ('ListItemControl', 'TreeItemControl', 'DataItemControl'):
                item_name = curr.Name
                break
            curr = curr.GetParentControl()

        if item_name:
            search_dirs = [
                os.path.join(os.path.expanduser('~'), 'Desktop'),
                os.path.join(os.path.expanduser('~'), 'OneDrive', 'Desktop'),
                r"C:\Users\Public\Desktop",
                os.getcwd()
            ]
            for d in search_dirs:
                if not os.path.exists(d):
                    continue
                candidate = os.path.join(d, item_name)
                if os.path.exists(candidate):
                    return sanitize_path(candidate)
                try:
                    for f in os.listdir(d):
                        if f == item_name or os.path.splitext(f)[0] == item_name:
                            return sanitize_path(os.path.join(d, f))
                except Exception:
                    pass
    except Exception as e:
        print(f"[Detector] UI point detection note: {e}")

    return None

def safe_delete(target_path):
    """Robust multi-tier file/folder deletion."""
    target = sanitize_path(target_path)
    if not target or not os.path.exists(target):
        print(f"[Delete] File does not exist or invalid path: {target_path}")
        return False

    print(f"[Delete] Deleting target: {target}")

    # Tier 1: send2trash (Recycle Bin)
    try:
        from send2trash import send2trash
        send2trash(target)
        if not os.path.exists(target):
            print(f"[Delete] Successfully moved to trash via send2trash: {target}")
            return True
    except Exception as e:
        print(f"[Delete] send2trash error: {e}")

    # Tier 2: Win32 SHFileOperationW (Native Windows Recycle Bin)
    try:
        import ctypes
        from ctypes import wintypes

        FO_DELETE = 0x0003
        FOF_ALLOWUNDO = 0x0040
        FOF_NOCONFIRMATION = 0x0010
        FOF_SILENT = 0x0004
        FOF_NOERRORUI = 0x0400

        class SHFILEOPSTRUCTW(ctypes.Structure):
            _fields_ = [
                ("hwnd", wintypes.HWND),
                ("wFunc", wintypes.UINT),
                ("pFrom", wintypes.LPCWSTR),
                ("pTo", wintypes.LPCWSTR),
                ("fFlags", ctypes.c_ushort),
                ("fAnyOperationsAborted", wintypes.BOOL),
                ("hNameMappings", wintypes.LPVOID),
                ("lpszProgressTitle", wintypes.LPCWSTR)
            ]

        file_op = SHFILEOPSTRUCTW()
        file_op.hwnd = None
        file_op.wFunc = FO_DELETE
        file_op.pFrom = target + "\0\0"
        file_op.pTo = None
        file_op.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT | FOF_NOERRORUI

        res = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(file_op))
        if res == 0 and not os.path.exists(target):
            print(f"[Delete] Successfully moved to trash via SHFileOperation: {target}")
            return True
    except Exception as e:
        print(f"[Delete] SHFileOperation error: {e}")

    # Tier 3: Direct filesystem removal
    try:
        if os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.remove(target)
        if not os.path.exists(target):
            print(f"[Delete] Successfully removed directly: {target}")
            return True
    except Exception as e:
        print(f"[Delete] Direct remove error: {e}")

    return False

def register_context_menu():
    try:
        exe_path = sys.executable
        if not exe_path.lower().endswith('.exe') or 'python' in exe_path.lower():
            exe_path = sys.executable
            script_path = os.path.abspath(__file__)
            command_str = f'"{exe_path}" "{script_path}" "%1"'
            icon_str = "shell32.dll,32"
        else:
            command_str = f'"{exe_path}" "%1"'
            icon_str = f'"{exe_path}",0'

        targets = [
            r"Software\Classes\*\shell\SummonDuckDeleter",
            r"Software\Classes\Directory\shell\SummonDuckDeleter",
            r"Software\Classes\Folder\shell\SummonDuckDeleter",
            r"Software\Classes\*\shell\SummonMonster",
            r"Software\Classes\Directory\shell\SummonMonster",
        ]

        for key_path in targets:
            try:
                key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
                winreg.SetValue(key, "", winreg.REG_SZ, "召喚可愛鴨鴨吃掉")
                winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, icon_str)
                winreg.CloseKey(key)

                cmd_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
                winreg.SetValue(cmd_key, "", winreg.REG_SZ, command_str)
                winreg.CloseKey(cmd_key)
            except Exception as e:
                print(f"Error registering key {key_path}: {e}")
    except Exception as e:
        print(f"Error in register_context_menu: {e}")

class SpriteAnimator(QLabel):
    animationFinished = pyqtSignal()
    frameChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.frames = []
        self.current_frame = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame)
        self.loop = True
        self.flip_horizontal = False
        self.is_playing = False

    def load_spritesheet(self, filepath, cols=COLS, rows=ROWS, target_height=DUCK_SIZE, frame_indices=None):
        transparent_path = filepath.replace(".png", "_transparent.png")
        if os.path.exists(transparent_path):
            filepath = transparent_path

        if not os.path.exists(filepath):
            print(f"Error: Sprite not found at {filepath}")
            return False

        image = QImage(filepath)
        if image.isNull():
            print(f"Error: Failed to load image {filepath}")
            return False

        pixmap = QPixmap.fromImage(image)

        frame_w = pixmap.width() // cols
        frame_h = pixmap.height() // rows

        self.frames = []
        for r in range(rows):
            for c in range(cols):
                frame = pixmap.copy(c * frame_w, r * frame_h, frame_w, frame_h)
                frame = frame.scaledToHeight(target_height, Qt.TransformationMode.SmoothTransformation)
                self.frames.append(frame)

        if frame_indices is not None:
            self.frames = [self.frames[i] for i in frame_indices if i < len(self.frames)]

        if self.frames:
            self.resize(self.frames[0].size())
        return True

    def set_flip(self, flip):
        self.flip_horizontal = flip
        self._update_frame()

    def play(self, fps=8, loop=True):
        self.loop = loop
        self.current_frame = 0
        self.is_playing = True
        self.timer.start(1000 // fps)
        self._update_frame()

    def stop(self):
        self.timer.stop()
        self.is_playing = False

    def next_frame(self):
        if not self.frames:
            return

        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            if self.loop:
                self.current_frame = 0
            else:
                self.current_frame = len(self.frames) - 1
                self.stop()
                self._update_frame()
                self.frameChanged.emit(self.current_frame)
                self.animationFinished.emit()
                return

        self._update_frame()
        self.frameChanged.emit(self.current_frame)

    def _update_frame(self):
        if not self.frames:
            return
        frame = self.frames[self.current_frame]
        if self.flip_horizontal:
            transform = QTransform().scale(-1, 1)
            frame = frame.transformed(transform, Qt.TransformationMode.SmoothTransformation)
        self.setPixmap(frame)


class BubbleWidget(QWidget):
    def __init__(self, text="呱？是要吃掉這個檔案嗎？✨", parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 18)
        self.lbl_text = QLabel(text)

        style = """
            QLabel {
                color: #4a3420; 
                padding: 18px 34px; 
                font-family: 'Segoe UI', 'Microsoft JhengHei', 'Microsoft YaHei', sans-serif; 
                font-size: 21px; 
                font-weight: 800;
            }
        """
        self.lbl_text.setStyleSheet(style)
        self.lbl_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_text)
        self.setLayout(layout)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setOffset(0, 10)
        shadow.setColor(QColor(255, 180, 50, 70))
        self.setGraphicsEffect(shadow)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()

        path = QPainterPath()
        path.addRoundedRect(3, 3, float(rect.width() - 6), float(rect.height() - 21), 26.0, 26.0)

        tail = QPainterPath()
        tail.moveTo(float(rect.width()) / 2 - 16, float(rect.height() - 21))
        tail.lineTo(float(rect.width()) / 2, float(rect.height() - 3))
        tail.lineTo(float(rect.width()) / 2 + 16, float(rect.height() - 21))
        path.addPath(tail)

        painter.setBrush(QColor(255, 253, 245, 252))
        painter.setPen(QPen(QColor(255, 195, 80, 230), 3.0))
        painter.drawPath(path)


class ChoicesWidget(QWidget):
    choiceMade = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        layout = QHBoxLayout()
        layout.setSpacing(16)

        self.btn1 = QPushButton("是的！吃掉它 🐥")
        self.btn2 = QPushButton("沒錯～就是這個 💖")

        btn_style = """
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffffff, stop:1 #fff5d6);
                color: #52381e; 
                border: 2.5px solid #ffbb44; 
                border-radius: 22px; 
                padding: 12px 28px; 
                font-family: 'Segoe UI', 'Microsoft JhengHei', 'Microsoft YaHei', sans-serif; 
                font-size: 17px; 
                font-weight: 800;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #ffd966, stop:1 #ffa91a);
                color: #ffffff;
                border: 2.5px solid #ea8b00;
            }
            QPushButton:pressed {
                background: #e67e22;
                color: #ffffff;
                border: 2.5px solid #d35400;
            }
        """
        self.btn1.setStyleSheet(btn_style)
        self.btn2.setStyleSheet(btn_style)

        for btn in [self.btn1, self.btn2]:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(20)
            shadow.setOffset(0, 8)
            shadow.setColor(QColor(255, 160, 30, 60))
            btn.setGraphicsEffect(shadow)

        self.btn1.clicked.connect(self.on_click)
        self.btn2.clicked.connect(self.on_click)

        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)
        self.setLayout(layout)

    def on_click(self):
        self.hide()
        self.choiceMade.emit()


class DuckDeleter(QWidget):
    def __init__(self, target_file=None):
        super().__init__()
        self.target_file = sanitize_path(target_file) if target_file else None
        self.target_pos = None
        self._bg_opacity = 0.0
        self.duck_sequence_started = False

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        screen = QApplication.primaryScreen().geometry()
        self.setGeometry(screen)

        self.animator = SpriteAnimator(self)
        self.animator.hide()

        self.explosion_animator = SpriteAnimator(self)
        self.explosion_animator.hide()

        self.bubble = BubbleWidget("呱？是要吃掉這個檔案嗎？✨")
        self.choices = ChoicesWidget()

        self.init_audio()
        self.init_targeting_ui()

    @pyqtProperty(float)
    def bg_opacity(self):
        return self._bg_opacity

    @bg_opacity.setter
    def bg_opacity(self, value):
        self._bg_opacity = value
        self.update()

    def init_audio(self):
        self.bgm_player = QMediaPlayer()
        self.bgm_audio = QAudioOutput()
        self.bgm_player.setAudioOutput(self.bgm_audio)
        bgm_path = get_asset_file("音频", "duck_bgm.mp3", "bgm(1).mp3")
        if os.path.exists(bgm_path):
            self.bgm_player.setSource(QUrl.fromLocalFile(bgm_path))
            self.bgm_audio.setVolume(0.45)
            self.bgm_player.mediaStatusChanged.connect(self.loop_bgm)

        self.sfx_player = QMediaPlayer()
        self.sfx_audio = QAudioOutput()
        self.sfx_player.setAudioOutput(self.sfx_audio)
        sfx_path = get_asset_file("音频", "duck_quack.mp3", "怪兽说话.mp3")
        if os.path.exists(sfx_path):
            self.sfx_player.setSource(QUrl.fromLocalFile(sfx_path))
            self.sfx_audio.setVolume(0.85)

        self.exp_player = QMediaPlayer()
        self.exp_audio = QAudioOutput()
        self.exp_player.setAudioOutput(self.exp_audio)
        exp_path = get_asset_file("音频", "duck_pop.mp3", "爆炸.MP4", "爆炸.mp3")
        if os.path.exists(exp_path):
            self.exp_player.setSource(QUrl.fromLocalFile(exp_path))
            self.exp_audio.setVolume(0.45)

    def loop_bgm(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.bgm_player.setPosition(0)
            self.bgm_player.play()

    def init_targeting_ui(self):
        cursor_size = 56
        cursor_pixmap = QPixmap(cursor_size, cursor_size)
        cursor_pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(cursor_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = cursor_size // 2
        radius = 20

        painter.setPen(QPen(QColor(255, 255, 255, 230), 4.5))
        painter.drawEllipse(center - radius, center - radius, radius * 2, radius * 2)

        painter.setPen(QPen(QColor(255, 150, 0, 245), 3.0))
        painter.drawEllipse(center - radius, center - radius, radius * 2, radius * 2)

        painter.setPen(QPen(QColor(255, 120, 0, 220), 2.5))
        painter.drawLine(center, 2, center, center - 7)
        painter.drawLine(center, center + 7, center, cursor_size - 2)
        painter.drawLine(2, center, center - 7, center)
        painter.drawLine(center + 7, center, cursor_size - 2, center)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(255, 210, 0)))
        painter.drawEllipse(center - 4, center - 4, 8, 8)

        painter.end()

        self.setCursor(QCursor(cursor_pixmap, center, center))

        self.fade_in_anim = QPropertyAnimation(self, b"bg_opacity")
        self.fade_in_anim.setDuration(800)
        self.fade_in_anim.setStartValue(0.0)
        self.fade_in_anim.setEndValue(0.40)
        self.fade_in_anim.start()

    def paintEvent(self, event):
        if self._bg_opacity > 0.01:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            bg_image_path = ""
            for ext in [".png", ".jpg", ".jpeg"]:
                test_path = get_resource_path(rf"assets\选择界面\选择界面{ext}")
                if os.path.exists(test_path):
                    bg_image_path = test_path
                    break

            if os.path.exists(bg_image_path):
                bg_image = QImage(bg_image_path)
                if not bg_image.isNull():
                    painter.setOpacity(self._bg_opacity)
                    scaled_img = bg_image.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                    x = (self.width() - scaled_img.width()) // 2
                    y = (self.height() - scaled_img.height()) // 2
                    painter.drawImage(x, y, scaled_img)
            else:
                painter.setOpacity(self._bg_opacity)
                painter.fillRect(self.rect(), QColor(255, 248, 230, 180))

            text_opacity = min(1.0, self._bg_opacity / 0.40)
            painter.setOpacity(text_opacity)

            font = QFont('Segoe UI', 28)
            font.setBold(True)
            painter.setFont(font)

            title_text = "請點擊要讓可愛鴨鴨吃掉的文件 🦆"

            painter.setPen(QColor(40, 20, 10, 170))
            painter.drawText(self.rect().adjusted(2, 2, 2, 2), Qt.AlignmentFlag.AlignCenter, title_text)

            painter.setPen(QColor(255, 255, 255, 255))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, title_text)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.on_app_exit()

    def mousePressEvent(self, event):
        if not self.duck_sequence_started and event.button() == Qt.MouseButton.LeftButton:
            self.target_pos = event.pos()
            self.duck_sequence_started = True
            self.setCursor(Qt.CursorShape.ArrowCursor)

            if not self.target_file:
                detected = resolve_file_at_point(event.globalPosition().toPoint().x(), event.globalPosition().toPoint().y())
                if detected:
                    self.target_file = detected
                    print(f"[Target] Resolved file at click: {self.target_file}")

            self.fade_out_anim = QPropertyAnimation(self, b"bg_opacity")
            self.fade_out_anim.setDuration(450)
            self.fade_out_anim.setStartValue(self._bg_opacity)
            self.fade_out_anim.setEndValue(0.0)
            self.fade_out_anim.finished.connect(self.init_duck_sequence)
            self.fade_out_anim.start()

    def init_duck_sequence(self):
        self.start_phase1_walk()

    def start_phase1_walk(self):
        if hasattr(self, 'bgm_player'):
            self.bgm_player.play()

        walk_sprite = get_asset_file("", "duck_walk_spritesheet.png", "走路动效_spritesheet.png")
        self.animator.load_spritesheet(walk_sprite, target_height=DUCK_SIZE)

        start_x = -self.animator.width()
        start_y = self.target_pos.y() - self.animator.height() // 2 + 50

        self.animator.set_flip(False)
        self.animator.move(start_x, start_y)
        self.animator.show()
        self.animator.play(fps=9, loop=True)

        self.move_anim = QPropertyAnimation(self.animator, b"pos")
        self.move_anim.setDuration(3600)

        end_x = self.target_pos.x() - self.animator.width() - 20
        self.move_anim.setStartValue(QPoint(start_x, start_y))
        self.move_anim.setEndValue(QPoint(end_x, start_y))
        self.move_anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.move_anim.finished.connect(self.start_phase2_point)
        self.move_anim.start()

    def start_phase2_point(self):
        if hasattr(self, 'sfx_player'):
            self.sfx_player.play()

        point_sprite = get_asset_file("", "duck_point_spritesheet.png", "指着文件_spritesheet.png")
        self.animator.load_spritesheet(point_sprite, target_height=DUCK_SIZE)

        try:
            self.animator.animationFinished.disconnect()
        except TypeError:
            pass

        self.animator.animationFinished.connect(self.show_dialog)
        self.animator.play(fps=10, loop=False)

    def show_dialog(self):
        try:
            self.animator.animationFinished.disconnect()
        except TypeError:
            pass

        global_pos = self.mapToGlobal(self.animator.pos())

        bubble_x = global_pos.x() + (self.animator.width() // 2) - 130
        bubble_y = global_pos.y() - 85
        self.bubble.move(bubble_x, bubble_y)
        self.bubble.show()

        choices_x = global_pos.x() + (self.animator.width() // 2) - 165
        choices_y = global_pos.y() + self.animator.height() - 10
        self.choices.move(choices_x, choices_y)

        try:
            self.choices.choiceMade.disconnect()
        except TypeError:
            pass

        self.choices.choiceMade.connect(self.start_phase3_kick)
        self.choices.show()

    def start_phase3_kick(self):
        self.bubble.hide()

        try:
            self.animator.animationFinished.disconnect()
            self.animator.frameChanged.disconnect()
        except TypeError:
            pass

        kick_sprite = get_asset_file("", "duck_kick_spritesheet.png", "踹文件动效_spritesheet.png")
        self.animator.load_spritesheet(kick_sprite, target_height=DUCK_SIZE)
        self.animator.animationFinished.connect(self.on_kick_finished)
        self.animator.frameChanged.connect(self.on_kick_frame)
        self.animator.play(fps=10, loop=False)

    def on_kick_frame(self, frame_idx):
        if frame_idx == 5:
            self.trigger_explosion()

    def trigger_explosion(self):
        if hasattr(self, 'exp_player'):
            self.exp_player.play()

        # Massive comic pop explosion
        pop_sprite = get_asset_file("", "duck_pop_spritesheet.png", "爆炸_spritesheet.png")
        self.explosion_animator.load_spritesheet(pop_sprite, target_height=EXPLOSION_SIZE)

        exp_x = self.target_pos.x() - self.explosion_animator.width() // 2
        exp_y = self.target_pos.y() - self.explosion_animator.height() // 2 - 30
        self.explosion_animator.move(exp_x, exp_y)
        self.explosion_animator.show()

        try:
            self.explosion_animator.animationFinished.disconnect()
        except TypeError:
            pass

        self.explosion_animator.animationFinished.connect(self.explosion_animator.hide)
        self.explosion_animator.play(fps=11, loop=False)

        # Trigger safe file deletion
        self.delete_target_file()

    def delete_target_file(self):
        if not self.target_file and self.target_pos:
            self.target_file = resolve_file_at_point(self.target_pos.x(), self.target_pos.y())

        if self.target_file:
            success = safe_delete(self.target_file)
            print(f"[Action] Deletion executed on: {self.target_file}, success={success}")
        else:
            print("[Action] No target file identified to delete.")

    def on_kick_finished(self):
        try:
            self.animator.animationFinished.disconnect()
            self.animator.frameChanged.disconnect()
        except TypeError:
            pass

        self.start_phase4_victory()

    def start_phase4_victory(self):
        victory_sprite = get_asset_file("", "duck_victory_spritesheet.png", "雷欧登场_spritesheet.png")
        self.animator.load_spritesheet(victory_sprite, target_height=DUCK_SIZE)
        self.animator.animationFinished.connect(self.start_phase5_fly)
        self.animator.play(fps=9, loop=False)

    def start_phase5_fly(self):
        try:
            self.animator.animationFinished.disconnect()
        except TypeError:
            pass

        fly_sprite = get_asset_file("", "duck_fly_spritesheet.png", "出场飞行动效_spritesheet.png")
        self.animator.load_spritesheet(fly_sprite, target_height=DUCK_SIZE)
        self.animator.play(fps=9, loop=True)

        screen = QApplication.primaryScreen().geometry()
        self.move_anim2 = QPropertyAnimation(self.animator, b"pos")
        self.move_anim2.setDuration(1800)
        self.move_anim2.setStartValue(self.animator.pos())

        end_x = screen.width() + 350
        end_y = self.animator.pos().y()

        self.move_anim2.setEndValue(QPoint(end_x, end_y))
        self.move_anim2.setEasingCurve(QEasingCurve.Type.InQuad)
        self.move_anim2.finished.connect(self.on_app_exit)
        self.move_anim2.start()

    def on_app_exit(self):
        try:
            self.bgm_player.stop()
            self.sfx_player.stop()
            self.exp_player.stop()
        except Exception:
            pass
        self.close()
        QApplication.quit()
        sys.exit(0)

# Backward compatibility alias
MonsterDeleter = DuckDeleter

if __name__ == '__main__':
    register_context_menu()

    target = None
    if len(sys.argv) >= 2:
        target = sys.argv[1]

    app = QApplication(sys.argv)
    ex = DuckDeleter(target)
    ex.show()
    sys.exit(app.exec())
