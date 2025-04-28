@echo off
REM Spostati nella cartella dello script
cd /d "%~dp0"

REM Controlla se Python è installato
where python >nul 2>nul
if errorlevel 1 (
    echo Errore: Python non è installato o non è aggiunto al PATH.
    echo Per favore installa Python da https://www.python.org/ e riprova.
    pause
    exit /b
)

REM Controlla se pip è disponibile
python -m ensurepip >nul 2>nul

REM Controlla se Streamlit è installato
python -c "import streamlit" >nul 2>nul
if errorlevel 1 (
    echo Streamlit non trovato. Installazione in corso...
    python -m pip install streamlit
)

REM Usa python per lanciare streamlit
python -m streamlit run word_finder.py

pause

