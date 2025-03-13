#!/bin/bash

echo "🚀 Pārbaude: Flask servera statuss"

# ✅ Pārbauda, vai Flask serveris darbojas
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://0.0.0.0:10000/)
if [ "$RESPONSE" -eq 200 ]; then
    echo "✅ Flask serveris darbojas!"
else
    echo "❌ Flask serveris NAV pieejams! (HTTP $RESPONSE)"
fi

# ✅ Pārbauda, vai OpenAI API atslēga ir iestatīta
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY nav iestatīts!"
else
    echo "✅ OPENAI_API_KEY ir iestatīts!"
fi

# ✅ Pārbauda instalētās Python atkarības
echo "🔍 Pārbaudām instalētās Python bibliotēkas..."
pip list | grep -E "flask|gunicorn|openai|httpx|urllib3|requests"

echo "🔍 Pārbaudām, vai ports 10000 ir atvērts..."
ss -tulnp | grep :10000 || echo "❌ Ports 10000 NAV atvērts!"

echo "✅ Pārbaude pabeigta!"
