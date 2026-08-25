import sys
import os
import uiautomation as auto

sys.stdout.reconfigure(encoding='utf-8')

def find_file_at_point(x, y):
    try:
        control = auto.ControlFromPoint(x, y)
        print(f"Control at ({x}, {y}): {control.Name}, ClassName={control.ClassName}, ControlType={control.ControlTypeName}")
        
        # Traverse up to find ListItemControl or TreeItemControl
        curr = control
        while curr:
            if isinstance(curr, (auto.ListItemControl, auto.TreeItemControl)) or curr.ControlTypeName in ('ListItemControl', 'TreeItemControl'):
                print(f"Found item: {curr.Name}")
                return curr.Name
            curr = curr.GetParentControl()
            
    except Exception as e:
        print(f"Error: {e}")
    return None

def find_selected_explorer_file():
    """Query active explorer / desktop window for selected file."""
    try:
        import win32com.client
    except ImportError:
        pass
        
    try:
        desktop = auto.GetRootControl()
        # Find selected item on desktop or active window
        for item, depth in auto.WalkTree(desktop, getChildren=lambda c: c.GetChildren(), maxDepth=6):
            if isinstance(item, (auto.ListItemControl, auto.TreeItemControl)):
                try:
                    pattern = item.GetSelectionItemPattern()
                    if pattern and pattern.IsSelected:
                        print(f"Selected item found: {item.Name}")
                        return item.Name
                except Exception:
                    pass
    except Exception as e:
        print(f"Selection error: {e}")
    return None

if __name__ == '__main__':
    # Test with current cursor position
    pt = auto.GetCursorPos()
    print("Current cursor:", pt)
    find_file_at_point(pt[0], pt[1])
    find_selected_explorer_file()
