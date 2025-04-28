#!/bin/bash

# Spostati nella cartella dove si trova questo script
cd "$(dirname "$0")"

# Controlla se Python è installato
if ! command -v python3 &> /dev/null; then
    echo "Python3 non è installato. Installalo prima di continuare."
    read -p "Premi INVIO per chiudere..."
    exit 1
fi

# Se myenv non esiste, crea l'ambiente virtuale
if [ ! -d "myenv" ]; then
    echo "Creo un ambiente virtuale (myenv)..."
    python3 -m venv myenv
fi

# Attiva l'ambiente virtuale
source ./myenv/bin/activate

# Controlla se Streamlit è installato nell'ambiente virtuale
if ! pip show streamlit &> /dev/null; then
    echo "Streamlit non trovato, lo installo..."
    pip install streamlit
fi

# Esegui Streamlit
streamlit run ./word_finder.py

# Attendi prima di chiudere
read -p "Premi INVIO per chiudere..."

