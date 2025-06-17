#!/bin/bash

echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "🐍 Installing Python3 and pip..."
sudo apt install -y python3 python3-pip

echo "🌐 Installing Flask..."
pip3 install Flask

echo "📁 Creating project directory..."
mkdir -p ~/pythonwebapp
cd ~/pythonwebapp

echo "📝 Creating Flask app..."
cat <<EOF > app.py
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello from PDF team. You have been hacked! 🚀"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF

echo "🚀 Starting Flask server..."
python3 app.py
