[Setup]
AppName=XCC的鼠小侠
AppVersion=1.0
DefaultDirName={pf}\XCC的鼠小侠
DefaultGroupName=XCC的鼠小侠
OutputDir=installer
OutputBaseFilename=XCC的鼠小侠_安装程序
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\XCC的鼠小侠.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\XCC的鼠小侠"; Filename: "{app}\XCC的鼠小侠.exe"
Name: "{commondesktop}\XCC的鼠小侠"; Filename: "{app}\XCC的鼠小侠.exe"

[Run]
Filename: "{app}\XCC的鼠小侠.exe"; Description: "启动 XCC的鼠小侠"; Flags: postinstall nowait 