; Inno Setup Script for DuckDeleter (可愛插畫鴨鴨檔案刪除助手)
#define MyAppName "DuckDeleter"
#define MyAppDisplayName "可愛插畫鴨鴨檔案刪除助手"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "apple595201908"
#define MyAppURL "https://github.com/apple595201908/DuckDeleter"
#define MyAppExeName "DuckDeleter.exe"

[Setup]
; Unique application GUID
AppId={{A95C953E-7286-4F17-8B3B-582E515BD0C9}
AppName={#MyAppDisplayName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={localappdata}\Programs\{#MyAppName}
DefaultGroupName={#MyAppDisplayName}
AllowNoIcons=yes
OutputDir=.
OutputBaseFilename=DuckDeleter_Setup_v1.0.0
SetupIconFile=assets\app_icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
UninstallDisplayIcon={app}\app_icon.ico

[Tasks]
Name: "desktopicon"; Description: "建立桌面捷徑"; Flags: unchecked

[Files]
Source: "DuckDeleter.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppDisplayName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app_icon.ico"
Name: "{group}\解除安裝 {#MyAppDisplayName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppDisplayName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\app_icon.ico"; Tasks: desktopicon

[Registry]
; Right-click on any file
Root: HKCU; Subkey: "Software\Classes\*\shell\SummonDuckDeleter"; ValueType: string; ValueName: ""; ValueData: "召喚可愛鴨鴨吃掉 🦆"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\*\shell\SummonDuckDeleter"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\DuckDeleter.exe"",0"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\*\shell\SummonDuckDeleter\command"; ValueType: string; ValueName: ""; ValueData: """{app}\DuckDeleter.exe"" ""%1"""; Flags: uninsdeletekey

; Right-click on directories
Root: HKCU; Subkey: "Software\Classes\Directory\shell\SummonDuckDeleter"; ValueType: string; ValueName: ""; ValueData: "召喚可愛鴨鴨吃掉 🦆"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Directory\shell\SummonDuckDeleter"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\DuckDeleter.exe"",0"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Directory\shell\SummonDuckDeleter\command"; ValueType: string; ValueName: ""; ValueData: """{app}\DuckDeleter.exe"" ""%1"""; Flags: uninsdeletekey

; Right-click on Folder
Root: HKCU; Subkey: "Software\Classes\Folder\shell\SummonDuckDeleter"; ValueType: string; ValueName: ""; ValueData: "召喚可愛鴨鴨吃掉 🦆"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Folder\shell\SummonDuckDeleter"; ValueType: string; ValueName: "Icon"; ValueData: """{app}\DuckDeleter.exe"",0"; Flags: uninsdeletekey
Root: HKCU; Subkey: "Software\Classes\Folder\shell\SummonDuckDeleter\command"; ValueType: string; ValueName: ""; ValueData: """{app}\DuckDeleter.exe"" ""%1"""; Flags: uninsdeletekey

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "立即啟動 {#MyAppDisplayName}"; Flags: nowait postinstall skipifsilent
