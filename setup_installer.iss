[Setup]
AppName=CryptCleaner
AppVersion=1.0
DefaultDirName={commonpf}\CryptCleaner
DefaultGroupName=CryptCleaner
OutputDir=.
OutputBaseFilename=CryptCleanerInstaller
Compression=lzma
SolidCompression=yes

[Files]
Source: "C:\Users\Lucas\Desktop\TCC\cryptCleaner\decoy\gui.pyw"; DestDir: "{app}\decoy"; Flags: ignoreversion
Source: "C:\Users\Lucas\Desktop\TCC\cryptCleaner\src\*"; DestDir: "{app}\src"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Lucas\Desktop\TCC\cryptCleaner\icons\*"; DestDir: "{app}\icons"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Lucas\Desktop\TCC\cryptCleaner\certs\*"; DestDir: "{app}\certs"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Lucas\Desktop\TCC\cryptCleaner\data\*"; DestDir: "{app}\data"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "C:\Users\Lucas\Desktop\TCC\cryptCleaner\qr_code.png"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\CryptCleaner"; Filename: "{app}\decoy\gui.pyw"; WorkingDir: "{app}"; IconFilename: "{app}\icons\clean.png"
Name: "{commondesktop}\CryptCleaner"; Filename: "{app}\decoy\gui.pyw"; WorkingDir: "{app}"; IconFilename: "{app}\icons\clean.png"

[Run]
Filename: "{app}\decoy\gui.pyw"; Description: "Run CryptCleaner"; Flags: nowait postinstall skipifsilent shellexec
