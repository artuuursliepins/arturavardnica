#!/bin/bash
echo "🚀 Starting Gunicorn server..."
gunicorn -w 4 -b 0.0.0.0:10000 server:app &

# ✅ Diagnosticējiet servera darbību
sleep 5
curl -X GET http://0.0.0.0:10000/
netstat -tulnp | grep :10000
pip list | grep -E "flask|gunicorn|openai"