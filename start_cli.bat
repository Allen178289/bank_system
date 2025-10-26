@echo off
chcp 65001 >nul
title 银行卡管理系统 命令行版

echo ============================================
echo    银行卡管理系统 v2.0 - 命令行版本
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

REM 启动命令行程序
python main.py

if errorlevel 1 (
    echo.
    echo [错误] 程序运行出错
    echo.
    pause
)

