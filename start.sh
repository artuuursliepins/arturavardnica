#!/bin/bash

pip install --upgrade pip

echo "🚀 Checking for pip installation..."
if ! command -v pip3 &> /dev/null; then
    apt-get update
    apt-get install -y python3-pip
fi

echo "🚀 Checking for Gunicorn installation..."
if ! pip3 show gunicorn &> /dev/null; then
    pip3 install gunicorn
fi

gunicorn --workers=4 --bind=0.0.0.0:10000 server:app --timeout 120
gunicorn -w 4 -b 0.0.0.0:$PORT server:app --timeout 120

echo "🚀 Starting Gunicorn server..."
gunicorn -w 4 -b 0.0.0.0:10000 server:app &

# ✅ Pārbauda, vai ports ir atvērts
sleep 5
curl -X GET http://0.0.0.0:10000/

# ✅ Pārbauda Flask un Gunicorn instalāciju
pip list | grep -E "flask|gunicorn|openai"

echo $OPENAI_API_KEY

@app.route("/process_text", methods=["POST"])
def process_text():
    """ 📌 Pārveido tekstu par SEO draudzīgu un semantiski korektu HTML, izmantojot OpenAI API """
    data = request.get_json()
    print("🔍 Saņemts pieprasījums:", data)  # ✅ Šis palīdzēs redzēt pieprasījuma datus
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "❌ Tukšs saturs! Lūdzu, ievadiet tekstu."}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Tu esi AI, kas pārveido tekstu uz HTML."},
                {"role": "user", "content": text}
            ],
            temperature=0
        )

        print("✅ OpenAI atbilde:", response.choices[0].message.content)  # ✅ Redzēt OpenAI atbildi terminālī

        return jsonify({"message": "✅ Teksts apstrādāts!", "html_content": response.choices[0].message.content})

    except Exception as e:
        print(f"🚨 Kļūda: {str(e)}")  # ✅ Izvada kļūdas konsolē
        return jsonify({"error": f"🚨 Servera kļūda: {str(e)}"}), 500
curl -X POST http://localhost:10000/process_text -H "Content-Type: application/json" -d '{"text": "Pārbaudes teksts"}'


bash check_status.sh

