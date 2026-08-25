import os
import sys
import winreg

def add_context_menu():
    try:
        # Get absolute paths
        python_exe = sys.executable
        if python_exe.lower().endswith("python.exe"):
            pythonw_exe = python_exe[:-10] + "pythonw.exe"
            if os.path.exists(pythonw_exe):
                python_exe = pythonw_exe

        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "main.py")
        exe_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "DuckDeleter.exe")

        if os.path.exists(exe_path):
            command_str = f'"{exe_path}" "%1"'
            icon_str = f'"{exe_path}",0'
        else:
            command_str = f'"{python_exe}" "{script_path}" "%1"'
            icon_str = "shell32.dll,32"

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

                command_key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path + r"\command")
                winreg.SetValue(command_key, "", winreg.REG_SZ, command_str)
                winreg.CloseKey(command_key)
            except Exception as e:
                print(f"Error registering {key_path}: {e}")

        print("Successfully registered all context menu entries!")
    except Exception as e:
        print(f"Error adding context menu: {e}")

if __name__ == "__main__":
    add_context_menu()
