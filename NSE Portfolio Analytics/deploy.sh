#!/bin/bash

# NSE Portfolio Analytics - Quick Deploy Script
# This script sets up and runs the portfolio analytics application

echo "🚀 NSE Portfolio Analytics - Quick Deploy"
echo "========================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "❌ pip is not installed. Please install pip and try again."
    exit 1
fi

echo "✅ Python and pip found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"

# Create data directory
mkdir -p data
echo "📁 Created data directory"

# Run basic test
echo "🧪 Running basic test..."
python3 -c "
import yfinance as yf
import pandas as pd
import streamlit
print('✅ All imports successful')

# Test data fetch
try:
    test_data = yf.download('RELIANCE.NS', period='5d', progress=False)
    if not test_data.empty:
        print('✅ Data fetch test successful')
    else:
        print('⚠️ Data fetch returned empty result (might be market closed)')
except Exception as e:
    print(f'⚠️ Data fetch test failed: {e}')
"

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "🚀 To start the application:"
echo "   streamlit run app.py"
echo ""
echo "📱 The app will be available at: http://localhost:8501"
echo ""
echo "🐳 To run with Docker:"
echo "   docker build -t nse-portfolio ."
echo "   docker run -p 8501:8501 nse-portfolio"
echo ""
echo "💡 Sample portfolios are pre-loaded in the application"
echo "📊 Try the 'NIFTY Top 10' sample portfolio to get started"
echo ""
echo "⚠️ Note: Market data is fetched from Yahoo Finance"
echo "   Data may not be available during market closed hours"