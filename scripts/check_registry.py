import winreg
import sys

sys.stdout.reconfigure(encoding='utf-8')

keys_to_check = [
    r"Software\Classes\*\shell\SummonDuckDeleter",
    r"Software\Classes\Directory\shell\SummonDuckDeleter",
    r"Software\Classes\Folder\shell\SummonDuckDeleter",
    r"Software\Classes\*\shell\SummonMonster",
    r"Software\Classes\Directory\shell\SummonMonster",
]

for k in keys_to_check:
    try:
        h = winreg.OpenKey(winreg.HKEY_CURRENT_USER, k)
        val = winreg.QueryValue(h, "")
        cmd_h = winreg.OpenKey(h, "command")
        cmd_val = winreg.QueryValue(cmd_h, "")
        print(f"FOUND {k}: '{val}' -> {cmd_val}")
        winreg.CloseKey(cmd_h)
        winreg.CloseKey(h)
    except Exception as e:
        print(f"NOT FOUND {k}: {e}")
