#!/bin/bash

echo "🚀 Starting Flask web server (app.py) on port 5001..."
python3 app.py > logs/flask.log 2>&1 &

