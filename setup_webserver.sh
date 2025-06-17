#!/bin/bash

echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "🐍 Installing Python3 and pip..."
sudo apt install -y python3 python3-pip

echo "🐍 Setting up Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

echo "🌐 Installing Flask..."
pip install Flask

echo "🚀 Starting Flask server..."
python3 app.py
