# filepath: /workspaces/arturavardnica/start.sh
#!/bin/bash

# Install pip if not already installed
sudo apt-get update
sudo apt-get install -y python3-pip

# Install gunicorn if not already installed
pip3 install gunicorn

echo "🚀 Starting Gunicorn server..."
/home/codespace/.local/bin/gunicorn -c /workspaces/arturavardnica/gunicorn_config.py server:app &

# ✅ Diagnosticējiet servera darbību
sleep 5
curl -X GET http://0.0.0.0:10000/
netstat -tulnp | grep :10000
pip list | grep -E "flask|gunicorn|openai"