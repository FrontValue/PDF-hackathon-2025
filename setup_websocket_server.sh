echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

echo "🐍 Installing Python3 and pip..."
sudo apt install -y python3 python3-pip

echo "🐍 Installing Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

echo "🌐 Installing websockets module..."
pip install websockets

echo "📝 Starting WebSocket echo server..."
python3 echo_server.py

echo "🚀 WebSocket server is ready to receive connections on ws://<your-pi-ip>:8765.