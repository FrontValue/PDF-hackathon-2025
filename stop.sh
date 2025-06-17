#!/bin/bash

echo "🛑 Stopping Flask app (app.py)..."
pkill -f app.py

echo "🛑 Stopping video stream server (video_stream_server.py)..."
pkill -f video_stream_server.py

# Optional: kill any leftover camera-run processes
echo "🛑 Stopping camera threads or related Python tasks..."
pkill -f 'camera.run'

echo "✅ All servers stopped."

