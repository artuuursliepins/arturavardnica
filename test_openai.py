import openai
import os
import json
import requests

# 🔑 Ielādē API atslēgu no Render
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("❌ OPENAI_API_KEY nav definēts vidē!")

# 🔧 Definē galveni
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 🔍 Izveido JSON pieprasījumu OpenAI API
data = {
    "model": "gpt-4o",
    "messages": [
        {"role": "system", "content": "Tu esi matemātisko simbolu vārdnīca."},
        {"role": "user", "content": "Kas ir integrāļa simbols?"}
    ],
    "temperature": 0.7,
    "max_tokens": None,  # ⚠️ Neierobežots apjoms
    "n": 1
}

# 🔄 Nosūta pieprasījumu OpenAI API
response = requests.post("https://api.openai.com/v1/chat/completions",
                         headers=headers, data=json.dumps(data))

# 📝 Izdrukā rezultātu
print(json.dumps(response.json(), indent=4, ensure_ascii=False))