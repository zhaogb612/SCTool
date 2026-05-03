@echo off
chcp 65001
echo 开始打包SCTools...
echo.

pyinstaller --clean --noconfirm --onedir --windowed ^
    --name "SCTools" ^
    --icon "src/resources/工具.png" ^
    --add-data "src/tools;src/tools" ^
    --add-data "src/navigation;src/navigation" ^
    --add-data "src/resources;src/resources" ^
    --collect-all PyQt5 ^
    main.py

echo.
echo 打包完成！
echo 可执行文件位于 dist/SCTools/SCTools.exe
pause
