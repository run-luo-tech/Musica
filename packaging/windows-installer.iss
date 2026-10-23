; Keep AppId stable across releases: this is also the uninstall registry identity.
#ifndef AppVersion
  #error AppVersion must be supplied by build_windows.ps1
#endif
#ifndef ReleaseDir
  #error ReleaseDir must be supplied by build_windows.ps1
#endif
#ifndef OutputDir
  #error OutputDir must be supplied by build_windows.ps1
#endif

[Setup]
AppId=Musica.Windows
AppName=Musica
AppVersion={#AppVersion}
AppVerName=Musica {#AppVersion}
AppPublisher=run-luo-tech
AppPublisherURL=https://github.com/run-luo-tech/Musica
AppSupportURL=https://github.com/run-luo-tech/Musica/issues
AppUpdatesURL=https://github.com/run-luo-tech/Musica/releases/latest
DefaultDirName={localappdata}\Programs\Musica
DefaultGroupName=Musica
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
MinVersion=10.0
UsePreviousAppDir=yes
DisableDirPage=no
AppendDefaultDirName=no
DisableProgramGroupPage=yes
WizardStyle=modern
DisableWelcomePage=no
OutputDir={#OutputDir}
OutputBaseFilename=Musica-Setup-{#AppVersion}
VersionInfoVersion={#AppVersion}.0
UninstallDisplayIcon={app}\Musica.exe
Compression=lzma2
SolidCompression=yes
CloseApplications=yes
CloseApplicationsFilter=Musica.exe
RestartApplications=no
SetupLogging=yes

[Languages]
Name: "chinesesimplified"; MessagesFile: "ChineseSimplified.isl"

[Messages]
WelcomeLabel1=欢迎安装 Musica {#AppVersion}
WelcomeLabel2=本安装包支持首次安装和旧版升级。%n%n升级前请退出 Musica 并备份 data 文件夹。v0.2.0 便携版用户请在下一步选择原 Musica.exe 所在文件夹，保留原曲库和设置。后续安装版升级将自动沿用已登记的位置。
SelectDirLabel3=首次安装可使用默认位置。升级 v0.2.0 便携版时，请选择原 Musica.exe 所在文件夹（其中应有 data 文件夹），不要另建一个空目录。
SelectDirBrowseLabel=安装或升级到以下文件夹。原有 data、config 和 exports 不会被覆盖。
FinishedLabel=Musica 安装或升级完成。
FinishedLabelNoIcons=可以从开始菜单打开 Musica。
ButtonNext=下一步(&N) >
ButtonBack=< 上一步(&B)
ButtonInstall=安装 / 升级(&I)
ButtonCancel=取消
ButtonFinish=完成(&F)
ButtonBrowse=浏览(&B)...

[Tasks]
Name: "desktopicon"; Description: "创建桌面快捷方式"; GroupDescription: "快捷方式："; Flags: unchecked

[Files]
Source: "{#ReleaseDir}\Musica.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ReleaseDir}\Windows-快速开始.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ReleaseDir}\THIRD_PARTY_NOTICES.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ReleaseDir}\Musica-使用说明书.pdf"; DestDir: "{app}"; Flags: ignoreversion
Source: "{#ReleaseDir}\licenses\*"; DestDir: "{app}\licenses"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{userprograms}\Musica"; Filename: "{app}\Musica.exe"; WorkingDir: "{app}"
Name: "{userdesktop}\Musica"; Filename: "{app}\Musica.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\Musica.exe"; Description: "启动 Musica"; Flags: nowait postinstall skipifsilent

[Code]
procedure InitializeWizard;
var
  Nearby: String;
begin
  // A portable download beside the old EXE is recognizable; never scan user disks.
  Nearby := ExtractFileDir(ExpandConstant('{srcexe}'));
  if (GetPreviousData('Installed', '') = '') and
     FileExists(Nearby + '\Musica.exe') and
     FileExists(Nearby + '\data\library.db') then
    WizardForm.DirEdit.Text := Nearby;
end;

procedure RegisterPreviousData(PreviousDataKey: Integer);
begin
  SetPreviousData(PreviousDataKey, 'Installed', 'yes');
end;
