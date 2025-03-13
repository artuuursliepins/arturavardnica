#!/bin/bash

# Install pip if not already installed
if ! command -v pip3 &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y python3-pip
fi

# Pārliecinās, ka Python ir instalēts
if ! command -v python &> /dev/null; then
    echo "❌ Python nav instalēts!"
    exit 1
fi

# Palaiž .pyz failu
python file.pyz

echo "✅ Process pabeigts!"

# Install gunicorn if not already installed
if ! pip3 show gunicorn &> /dev/null; then
    pip3 install gunicorn
fi

echo "🚀 Starting Gunicorn server..."
gunicorn -w 4 -b 0.0.0.0:10000 server:app &

# Wait for the server to start
sleep 5
curl -X GET http://0.0.0.0:10000/
netstat -tulnp | grep :10000
pip list | grep -E "flask|gunicorn|openai"

