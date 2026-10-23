@echo off
echo ======================================================
echo   SAF Explorer - Extraindo dados e reconstruindo app
echo ======================================================
echo.
echo 1/2: Extraindo planilhas de data/phantoms/...
python src/extract.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Falha ao extrair dados. Verifique os arquivos Excel.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo 2/2: Injetando dados no index.html...
python src/build.py
if %ERRORLEVEL% NEQ 0 (
    echo [ERRO] Falha ao construir o index.html.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ======================================================
echo   SUCESSO! Dados atualizados no index.html.
echo   Basta recarregar a pagina no navegador (F5 / Ctrl+F5).
echo ======================================================
echo.
pause
