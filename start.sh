#!/bin/bash

echo "🚀 Starting Flask web server (app.py) on port 5001..."
python3 app.py > logs/flask.log 2>&1 &

echo "📸 Starting video stream server (video_stream_server.py) on port 3002..."
python3 video_stream_server.py -p 3002 > logs/stream.log 2>&1 &

echo "🟢 Both servers started in background."
