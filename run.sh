#!/bin/bash
# Bot launcher script

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$SCRIPT_DIR"

# Check if .env file exists
if [ ! -f "$PROJECT_DIR/.env" ]; then
    echo "❌ .env file not found!"
    echo "   Please create .env file from .env.example"
    echo ""
    echo "   Steps:"
    echo "   1. cp .env.example .env"
    echo "   2. Edit .env and add your BOT_TOKEN"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$PROJECT_DIR/venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv "$PROJECT_DIR/venv"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$PROJECT_DIR/venv/bin/activate"

# Install requirements
echo "📥 Installing requirements..."
pip install -q -r "$PROJECT_DIR/requirements.txt"

# Run the bot
echo "🚀 Starting bot..."
cd "$PROJECT_DIR/src"
python main.py
