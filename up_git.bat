@echo off
cd /d %~dp0

echo ============================================
echo Atualizacao de arquivos em andamento...
echo ============================================

:: Cria .gitkeep em pastas vazias
for /f "delims=" %%d in ('dir /ad /b /s') do (
    dir /a /b "%%d" >nul 2>&1
    if errorlevel 1 (
        type nul > "%%d\.gitkeep"
    )
)

git add -A

git diff --cached --quiet
IF %ERRORLEVEL%==0 (
    echo Tudo atualizado e na ultima versao.
) ELSE (
    git commit -m "Auto update"
    git push
)

echo ============================================
echo FINALIZADO - Atualizacao de arquivos concluida.
echo ============================================
pause