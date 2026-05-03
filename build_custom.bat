@echo off
chcp 65001
echo 开始打包SCTools...
echo.

rmdir /s /q dist
rmdir /s /q build
del /f /q SCTools.spec

echo 创建临时打包目录...
mkdir temp_dist

pyinstaller --clean --noconfirm --onedir --windowed ^
    --name "SCTools" ^
    --icon "src/resources/工具.png" ^
    --hidden-import PyQt5.QtWidgets ^
    --hidden-import PyQt5.QtGui ^
    --hidden-import PyQt5.QtCore ^
    main.py

echo 复制文件到临时目录...
xcopy /s /y "dist\SCTools\*" "temp_dist\" > nul

rem 复制资源文件
echo 复制资源文件...
xcopy /s /y "src\tools" "temp_dist\" > nul
xcopy /s /y "src\navigation" "temp_dist\" > nul
xcopy /s /y "src\resources" "temp_dist\" > nul

rem 删除原始dist目录并将临时目录重命名为dist
rmdir /s /q dist
rename temp_dist dist

echo.
echo 打包完成！
echo 可执行文件位于 dist/SCTools.exe
pause
