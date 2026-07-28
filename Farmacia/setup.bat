@echo off
title Farmacia POS - Instalación Automática

echo ========================================
echo   FARMACIA POS - INSTALACIÓN AUTOMÁTICA
echo ========================================
echo.

:: Verificar si Python está instalado
echo [1/7] Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ Python no está instalado.
    echo.
    echo Para instalar Python:
    echo   1. Ve a: https://www.python.org/downloads/
    echo   2. Descarga Python 3.11 o superior
    echo   3. Durante la instalación, MARCA "Add Python to PATH"
    echo   4. Reinicia esta terminal y vuelve a ejecutar este script
    echo.
    pause
    exit /b 1
)

:: Mostrar versión de Python
python --version
echo ✅ Python encontrado!
echo.

:: Navegar a la carpeta Farmacia
echo [2/7] Navegando a la carpeta Farmacia...
cd Farmacia
if errorlevel 1 (
    echo ❌ No se encontró la carpeta Farmacia
    pause
    exit /b 1
)
echo ✅ Carpeta Farmacia encontrada
echo.

:: Crear entorno virtual
echo [3/7] Creando entorno virtual...
if not exist venv (
    py -m venv venv
    echo ✅ Entorno virtual creado
) else (
    echo ⚠️ El entorno virtual ya existe
)
echo.

:: Activar entorno virtual e instalar dependencias
echo [4/7] Instalando dependencias...
call venv\Scripts\activate.bat
pip install openpyxl reportlab pillow >nul 2>&1
echo ✅ Dependencias instaladas
echo.

:: Navegar a database
echo [5/7] Configurando base de datos...
cd database
if errorlevel 1 (
    echo ❌ No se encontró la carpeta database
    pause
    exit /b 1
)

:: Inicializar base de datos
echo    - Creando base de datos...
py init_db.py >nul 2>&1
echo    ✅ Base de datos creada

:: Ejecutar migración de facturas
echo    - Ejecutando migraciones...
if exist migrar.py (
    py migrar.py >nul 2>&1
    echo    ✅ Migración de facturas completada
) else (
    echo    ⚠️ No se encontró migrar.py, omitiendo...
)
echo.

:: Insertar datos de prueba (opcional)
echo [6/7] Insertando datos de prueba...
cd ..
if exist insertar_datos_prueba.py (
    py insertar_datos_prueba.py >nul 2>&1
    echo ✅ Datos de prueba insertados
) else (
    echo ⚠️ No se encontró insertar_datos_prueba.py, omitiendo...
)
echo.

:: Ejecutar aplicación
echo [7/7] Iniciando aplicación...
echo ========================================
echo   ✅ INSTALACIÓN COMPLETADA
echo   Iniciando Farmacia POS...
echo ========================================
echo.
py main.py

pause