@echo off
chcp 65001
echo 开始打包SCTools...
echo.

rem 清理旧文件
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist SCTools.spec del /f /q SCTools.spec

rem 打包应用
pyinstaller --clean --noconfirm --onedir --windowed --name "SCTools" --icon "src/resources/工具.png" main.py

echo 复制资源文件...
xcopy /s /y "src\tools" "dist\SCTools\" > nul
xcopy /s /y "src\navigation" "dist\SCTools\" > nul
xcopy /s /y "src\resources" "dist\SCTools\" > nul

echo.
echo 打包完成！
echo 可执行文件位于 dist/SCTools/SCTools.exe
pause
