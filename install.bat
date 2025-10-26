@echo off
chcp 65001 >nul
title 银行卡管理系统 - 安装依赖

echo ============================================
echo    银行卡管理系统 v2.0 - 安装程序
echo ============================================
echo.

REM 检查Python是否安装
echo [1/3] 检查Python环境...
python --version
if errorlevel 1 (
    echo.
    echo [错误] 未检测到Python！
    echo 请先安装Python 3.6或更高版本
    echo 下载地址: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo.
echo [2/3] 升级pip...
python -m pip install --upgrade pip

echo.
echo [3/3] 安装依赖包...
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [错误] 安装失败！
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================
echo    安装完成！
echo ============================================
echo.
echo 您现在可以：
echo   1. 双击 start_gui.bat 启动GUI版本（推荐）
echo   2. 双击 start_cli.bat 启动命令行版本
echo   3. 或运行命令：python main_gui.py
echo.
pause

