#!/bin/bash

echo "🚀 Checking for pip installation..."
if ! command -v pip3 &> /dev/null; then
    apt-get update
    apt-get install -y python3-pip
fi

echo "🚀 Checking for Gunicorn installation..."
if ! pip3 show gunicorn &> /dev/null; then
    pip3 install gunicorn
fi

echo "🚀 Starting Gunicorn server..."
gunicorn -w 4 -b 0.0.0.0:10000 server:app &

# ✅ Pārbauda, vai ports ir atvērts
sleep 5
curl -X GET http://0.0.0.0:10000/

# ✅ Pārbauda Flask un Gunicorn instalāciju
pip list | grep -E "flask|gunicorn|openai"

bash check_status.sh

