; 脚本由 Inno Setup 脚本向导生成。
; 有关创建 Inno Setup 脚本文件的详细信息，请参阅帮助文档！
; 仅供非商业使用

#define MyAppName "ScTools"
#define MyAppVersion "1.0"
#define MyAppPublisher "沙尘612"
#define MyAppURL "zhaogb612.github.io"
#define MyAppExeName "SCTools.exe"

[Setup]
; 注意：AppId 的值唯一标识此应用程序。不要在其他应用程序的安装程序中使用相同的 AppId 值。
; (若要生成新的 GUID，请在 IDE 中单击 "工具|生成 GUID"。)
AppId={{6834D75D-8A10-4AFF-85DB-432491BFB851}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
; "ArchitecturesAllowed=x64compatible" 指定
; 安装程序只能在 x64 和 Windows 11 on Arm 上运行。
ArchitecturesAllowed=x64compatible
; "ArchitecturesInstallIn64BitMode=x64compatible" 要求
; 在 X64 或 Windows 11 on Arm 上以 "64-位模式" 进行安装，
; 这意味着它应该使用本地 64 位 Program Files 目录
; 和注册表的 64 位视图。
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
LicenseFile=D:\myblog\SCTools\许可证.txt
InfoBeforeFile=D:\myblog\SCTools\安装前信息.txt
InfoAfterFile=D:\myblog\SCTools\安装后信息.txt
; 取消注释以下行以在非管理安装模式下运行 (仅为当前用户安装)。
;PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=D:\myblog\SCTools\dist
OutputBaseFilename=ScTools_Setup
SetupIconFile=C:\Users\Z1321\Downloads\4444\批量抠图_37086818_标准_0.ico
SolidCompression=yes
WizardStyle=modern dark polar
; 启用覆盖更新功能
CreateUninstallRegKey=yes
Uninstallable=yes
; 支持Windows 10及以上版本
MinVersion=10.0

[Languages]
Name: "chinesesimp"; MessagesFile: "compiler:Default.isl"
Name: "english"; MessagesFile: "compiler:Languages\English.isl"

[CustomMessages]
chinesesimp.AdditionalIcons=创建桌面快捷方式
chinesesimp.AssocFileExtension=关联文件扩展名
chinesesimp.AssocingFileExtension=正在关联文件扩展名 {#MyAppExt}...

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: "D:\myblog\SCTools\dist\SCTools\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\myblog\SCTools\dist\SCTools\_internal\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 注意：不要在任何共享系统文件上使用 "Flags: ignoreversion" 

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// 自定义代码段 - 实现覆盖更新功能
var
  PreviousVersion: string;
  IsUpdate: Boolean;

function InitializeSetup(): Boolean;
begin
  // 检查是否已安装旧版本
  IsUpdate := False;
  if RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{6834D75D-8A10-4AFF-85DB-432491BFB851}_is1') then
  begin
    // 获取已安装的版本号
    if RegQueryStringValue(HKEY_LOCAL_MACHINE, 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\{6834D75D-8A10-4AFF-85DB-432491BFB851}_is1', 'DisplayVersion', PreviousVersion) then
    begin
      IsUpdate := True;
      
      // 显示更新提示
      if MsgBox('检测到已安装的 ScTools 版本 ' + PreviousVersion + '。是否继续安装新版本？', mbConfirmation, MB_YESNO) = IDYES then
      begin
        Result := True;
      end
      else
      begin
        Result := False;
      end;
    end
    else
    begin
      Result := True;
    end;
  end
  else
  begin
    Result := True;
  end;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  // 在安装过程中处理覆盖更新
  if CurStep = ssInstall then
  begin
    // 如果存在旧版本，先尝试卸载
    if IsUpdate then
    begin
      // 停止可能正在运行的程序
      Exec('taskkill', '/f /im SCTools.exe', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
      
      // 延迟一下确保程序完全关闭
      Sleep(1000);
      
      // 显示更新进度
      WizardForm.StatusLabel.Caption := '正在更新 ScTools...';
      
      // 备份用户数据
      BackupUserData();
    end;
  end
  else if CurStep = ssPostInstall then
  begin
    // 安装完成后恢复用户数据
    if IsUpdate then
    begin
      RestoreUserData();
    end;
  end;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
begin
  // 如果是更新安装，跳过某些页面
  if IsUpdate then
  begin
    if (PageID = wpSelectDir) or (PageID = wpSelectProgramGroup) then
    begin
      // 更新时使用相同的安装目录和程序组
      Result := True;
    end
    else
    begin
      Result := False;
    end;
  end
  else
  begin
    Result := False;
  end;
end;

procedure DeinitializeSetup();
begin
  // 安装完成后清理临时文件
  DeleteFile(ExpandConstant('{tmp}\\安装前信息.txt'));
  DeleteFile(ExpandConstant('{tmp}\\安装后信息.txt'));
end;

// 自定义函数：检查文件是否被占用
function IsFileInUse(const FileName: string): Boolean;
var
  HFileRes: THandle;
begin
  Result := False;
  if FileExists(FileName) then
  begin
    HFileRes := CreateFile(PChar(FileName), GENERIC_READ or GENERIC_WRITE, 0, nil, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, 0);
    Result := (HFileRes = INVALID_HANDLE_VALUE);
    if not Result then
      CloseHandle(HFileRes);
  end;
end;

// 自定义函数：强制删除文件
function ForceDeleteFile(const FileName: string): Boolean;
begin
  Result := True;
  if FileExists(FileName) then
  begin
    // 先尝试正常删除
    if not DeleteFile(FileName) then
    begin
      // 如果正常删除失败，尝试强制删除
      if not RemoveFile(FileName) then
      begin
        MsgBox('无法删除文件: ' + FileName, mbError, MB_OK);
        Result := False;
      end;
    end;
  end;
end;

// 自定义函数：备份用户数据
procedure BackupUserData();
var
  AppDataPath: string;
  BackupPath: string;
begin
  AppDataPath := ExpandConstant('{userappdata}\\ScTools');
  BackupPath := ExpandConstant('{app}\\Backup');
  
  if DirExists(AppDataPath) then
  begin
    // 创建备份目录
    ForceDirectories(BackupPath);
    
    // 复制用户数据到备份目录 - 使用正确的文件复制方法
    if not DirCopy(AppDataPath, BackupPath, True) then
    begin
      Log('备份用户数据失败');
    end
    else
    begin
      Log('用户数据已备份到: ' + BackupPath);
    end;
  end;
end;

// 自定义函数：恢复用户数据
procedure RestoreUserData();
var
  AppDataPath: string;
  BackupPath: string;
begin
  AppDataPath := ExpandConstant('{userappdata}\\ScTools');
  BackupPath := ExpandConstant('{app}\\Backup');
  
  if DirExists(BackupPath) then
  begin
    // 确保目标目录存在
    ForceDirectories(AppDataPath);
    
    // 从备份目录恢复用户数据 - 使用正确的目录复制方法
    if not DirCopy(BackupPath, AppDataPath, True) then
    begin
      Log('恢复用户数据失败');
    end
    else
    begin
      Log('用户数据已从备份恢复');
      
      // 删除备份目录
      DelTree(BackupPath, True, True, True);
    end;
  end;
end;

// 自定义函数：检查是否需要重启
function NeedRestart(): Boolean;
begin
  // 如果检测到文件被占用，可能需要重启
  Result := IsFileInUse(ExpandConstant('{app}\\{#MyAppExeName}'));
end;

