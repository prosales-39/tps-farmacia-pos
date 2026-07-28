@echo off
title Farmacia POS - Instalacion
echo ========================================
echo   FARMACIA POS - Instalacion
echo ========================================
echo.

:: Obtener ruta actual
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"
set "CURRENT_DIR=%CD%"

echo Ruta actual: %CURRENT_DIR%
echo.

:: Verificar si estamos en Farmacia o en la raiz
set "FARMACIA_DIR="

if exist "%CURRENT_DIR%\Farmacia" (
    set "FARMACIA_DIR=%CURRENT_DIR%\Farmacia"
    echo Encontrado: Farmacia en la carpeta actual
)

:: Si no encontramos Farmacia, verificar si estamos dentro de Farmacia
if "%FARMACIA_DIR%"=="" (
    if exist "%CURRENT_DIR%\main.py" (
        set "FARMACIA_DIR=%CURRENT_DIR%"
        echo Encontrado: Estamos dentro de la carpeta Farmacia
    )
)

:: Si aun no encontramos, buscar hacia arriba
if "%FARMACIA_DIR%"=="" (
    set "SEARCH_DIR=%CURRENT_DIR%"
    :loop
    if exist "%SEARCH_DIR%\Farmacia\main.py" (
        set "FARMACIA_DIR=%SEARCH_DIR%\Farmacia"
        echo Encontrado: Farmacia en %SEARCH_DIR%
        goto found
    )
    set "SEARCH_DIR=%SEARCH_DIR%\.."
    if not "%SEARCH_DIR%"=="%CURRENT_DIR%" goto loop
)

:found
if "%FARMACIA_DIR%"=="" (
    echo Error: No se pudo encontrar la carpeta Farmacia
    echo.
    echo Asegurate de ejecutar este script desde:
    echo   - La raiz del proyecto
    echo   - O dentro de la carpeta Farmacia
    echo.
    pause
    exit /b 1
)

echo.
echo Carpeta Farmacia encontrada: %FARMACIA_DIR%
echo.

:: Entrar a Farmacia
cd /d "%FARMACIA_DIR%"

echo [1/5] Verificando Python...

python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo Error: Python no esta instalado
    echo.
    echo Instala Python desde: https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

python --version
echo.

:: Crear entorno virtual
echo [2/5] Creando entorno virtual...
if exist venv (
    echo El entorno virtual ya existe
) else (
    python -m venv venv
    echo Entorno virtual creado
)
echo.

:: Instalar dependencias
echo [3/5] Instalando dependencias...
call venv\Scripts\activate.bat
pip install openpyxl reportlab pillow
echo.
echo Dependencias instaladas
echo.

:: Configurar base de datos
echo [4/5] Configurando base de datos...
cd database
python init_db.py
cd ..
echo.

:: Ejecutar aplicacion
echo [5/5] Iniciando aplicacion...
echo.
echo ========================================
echo   Instalacion completada
echo   Iniciando Farmacia POS...
echo ========================================
echo.
echo Credenciales:
echo   Usuario: admin
echo   Contraseña: admin123
echo.

python main.py

pause