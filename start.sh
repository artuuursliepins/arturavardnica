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

# ✅ Pārbauda aktīvos savienojumus
netstat -an | grep 10000

# Pāriet uz projektu
cd mans_projekts

# Klonēt OpenAI Python pakotni (ja vēl nav)
git clone https://github.com/openai/openai-python.git openai

# Pievienot OpenAI pakotni GitHub repozitorijam
git add openai
git commit -m "Pievienots OpenAI avota kods"
git push origin main
