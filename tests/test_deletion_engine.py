import sys
import os
import urllib.parse

sys.stdout.reconfigure(encoding='utf-8')

def sanitize_path(path_str):
    if not path_str:
        return None
    cleaned = path_str.strip(' \t\r\n"\'')
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
    """Find currently selected file in any open Explorer window or Desktop."""
    try:
        import comtypes.client
        shell = comtypes.client.CreateObject("Shell.Application")
        for w in shell.Windows():
            try:
                doc = w.Document
                sel = doc.SelectedItems()
                if sel and sel.Count > 0:
                    item = sel.Item(0)
                    path = sanitize_path(item.Path)
                    if path:
                        return path
            except Exception:
                pass
    except Exception:
        pass
    return None

def find_file_from_point(x, y):
    """Find file/folder on Desktop or in Explorer located at screen coordinates (x, y)."""
    # 1. First check if any Explorer window has a selected item
    selected = find_file_from_explorer_selection()
    if selected:
        return selected
        
    # 2. Use UIAutomation to find control under (x, y)
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
            print(f"[Detector] UI Item found at ({x}, {y}): {item_name}")
            
            # Check user Desktop
            desktop_dirs = [
                os.path.join(os.path.expanduser('~'), 'Desktop'),
                r"C:\Users\Public\Desktop",
                os.getcwd()
            ]
            
            for d in desktop_dirs:
                if not os.path.exists(d):
                    continue
                # Exact match
                candidate = os.path.join(d, item_name)
                if os.path.exists(candidate):
                    return sanitize_path(candidate)
                # Match without extension (e.g. user sees 'abc' but file is 'abc.txt')
                for f in os.listdir(d):
                    if f == item_name or os.path.splitext(f)[0] == item_name:
                        return sanitize_path(os.path.join(d, f))
    except Exception as e:
        print(f"[Detector] Point detection error: {e}")
        
    return None

def safe_delete(target_path):
    """Robust 3-tier deletion (send2trash -> Win32 Shell API -> os.remove/rmtree)."""
    target = sanitize_path(target_path)
    if not target or not os.path.exists(target):
        print(f"[Delete] File not found or invalid: {target_path}")
        return False
        
    print(f"[Delete] Attempting to delete: {target}")
    
    # Tier 1: send2trash
    try:
        from send2trash import send2trash
        send2trash(target)
        if not os.path.exists(target):
            print(f"[Delete] Successfully moved to trash via send2trash: {target}")
            return True
    except Exception as e:
        print(f"[Delete] send2trash failed: {e}")
        
    # Tier 2: Win32 SHFileOperation (FO_DELETE with FOF_ALLOWUNDO)
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
        # Double null-terminated string required by SHFileOperation
        file_op.pFrom = target + "\0\0"
        file_op.pTo = None
        file_op.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT | FOF_NOERRORUI
        
        res = ctypes.windll.shell32.SHFileOperationW(ctypes.byref(file_op))
        if res == 0 and not os.path.exists(target):
            print(f"[Delete] Successfully moved to trash via SHFileOperation: {target}")
            return True
    except Exception as e:
        print(f"[Delete] SHFileOperation failed: {e}")
        
    # Tier 3: Direct removal
    try:
        import shutil
        if os.path.isdir(target):
            shutil.rmtree(target)
        else:
            os.remove(target)
        if not os.path.exists(target):
            print(f"[Delete] Successfully deleted directly: {target}")
            return True
    except Exception as e:
        print(f"[Delete] Direct removal failed: {e}")
        
    return False

if __name__ == '__main__':
    # Test on a dummy file
    dummy = os.path.join(os.path.expanduser('~'), 'Desktop', 'dummy_duck_test.txt')
    with open(dummy, 'w', encoding='utf-8') as f:
        f.write("test duck delete")
    print("Created test file:", dummy, os.path.exists(dummy))
    
    deleted = safe_delete(dummy)
    print("Deleted successfully?", deleted)
