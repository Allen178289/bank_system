@echo off
chcp 65001 >nul
title 银行卡管理系统 GUI版

echo ============================================
echo    银行卡管理系统 v2.0 - GUI版本
echo ============================================
echo.
echo 正在启动程序...
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到Python，请先安装Python 3.6或更高版本
    echo.
    pause
    exit /b 1
)

REM 检查PyQt5是否安装
python -c "import PyQt5" >nul 2>&1
if errorlevel 1 (
    echo [提示] 未检测到PyQt5，正在安装依赖...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [错误] 依赖安装失败
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [成功] 依赖安装完成
    echo.
)

REM 启动GUI程序
python main_gui.py

if errorlevel 1 (
    echo.
    echo [错误] 程序运行出错
    echo.
    pause
)

