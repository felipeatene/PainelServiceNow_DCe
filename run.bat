@echo off
echo Iniciando servidor Painel DC-e...
echo.
@REM Opcional: pre-configurar credenciais (evita digitar no formulario)
@REM set SN_USER=seu.usuario
@REM set SN_PASS=sua_senha
python "%~dp0server.py"
pause
