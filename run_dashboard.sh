#!/bin/bash

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "🖥️  Starting Modern System Dashboard..."
echo "📍 Location: $SCRIPT_DIR"


# Check if virtual environment exists, create if not
if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "📦 Virtual environment not found. Creating new venv..."
    python3.12 -m venv "$SCRIPT_DIR/venv"
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment. Make sure python3.12 is installed."
        exit 1
    fi
    echo "✅ Virtual environment created successfully!"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source "$SCRIPT_DIR/venv/bin/activate"

# Log the activated virtual environment
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Virtual environment activated: $(basename "$VIRTUAL_ENV")"
else
    echo "⚠️  Warning: Virtual environment activation may have failed"
    exit 1
fi

# Install required packages
echo "📦 Installing required Python packages..."
pip install "rich>=13.0.0" "psutil>=5.8.0"

# Make the Python script executable
chmod +x "$SCRIPT_DIR/system_dashboard.py"



# Launch the dashboard
echo "🚀 Launching dashboard..."
echo "   Press Ctrl+C to exit"
echo ""

cd "$SCRIPT_DIR"
python system_dashboard.py "$@"
