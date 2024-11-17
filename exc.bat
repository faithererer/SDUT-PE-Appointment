@echo off
:: 设置 cmd 的代码页为 UTF-8
chcp 65001 > nul
:: 设置虚拟环境的目录名
set VENV_DIR=venv

:: 检测虚拟环境是否存在
if not exist "%VENV_DIR%\" (
    echo [INFO] 虚拟环境未找到，正在创建虚拟环境...
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo [ERROR] 创建虚拟环境失败！
        exit /b 1
    )
    echo [INFO] 虚拟环境已创建。
) else (
    echo [INFO] 虚拟环境已存在。
)

:: 激活虚拟环境
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] 无法激活虚拟环境！
    exit /b 1
)

:: 检查 requirements.txt 是否存在
if not exist "requirements.txt" (
    echo [WARNING] 找不到 requirements.txt，跳过依赖安装。
) else (
    echo [INFO] 安装依赖...
    pip install --upgrade pip
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] 安装依赖失败！
        exit /b 1
    )
    echo [INFO] 依赖安装完成。
)

:: 运行 main.py
echo [INFO] 正在运行 main.py...
python main.py
if errorlevel 1 (
    echo [ERROR] main.py 执行失败！
    exit /b 1
)

echo [INFO] main.py 执行完成！
exit /b 0
