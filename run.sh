#!/bin/bash

# SpareBank 1 Lotteri - Startup Script

echo ""
echo "=========================================="
echo "  🎰 SpareBank 1 Lotteri"
echo "=========================================="
echo ""

# Sjekk om Python er installert
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 er ikke installert."
    echo "Last ned fra https://www.python.org/"
    exit 1
fi

echo "✓ Python finnes"

# Sjekk om venv finnes, hvis ikke lag den
if [ ! -d "venv" ]; then
    echo "📦 Setter opp virtuelt miljø..."
    python3 -m venv venv
fi

# Aktiver venv
echo "✓ Aktiverer virtuelt miljø"
source venv/bin/activate

# Installer/oppdater pakker
echo "📦 Installerer avhengigheter..."
pip install -q -r requirements.txt

# Start applikasjonen
echo ""
echo "🚀 Starter applikasjonen..."
echo ""
echo "📍 Åpne nettleseren på: http://localhost:5000"
echo ""
echo "Trykk CTRL+C for å stoppe applikasjonen."
echo ""

python3 app.py
