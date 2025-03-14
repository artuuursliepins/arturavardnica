from flask import Flask, request, jsonify, render_template
import os
from openai import OpenAI

# 🚀 API atslēga tiek ielādēta no Render Environment Variables vai GitHub Secrets
api_key = os.getenv("OPENAI_API_KEY") or os.getenv("GITHUB_API_KEY")
if not api_key:
    raise ValueError("❌ Kļūda: OpenAI API atslēga nav atrasta Render vidē vai GitHub Secrets!")

# ✅ OpenAI API inicializācija
client = OpenAI()

# 📂 Direktorijas failiem
UPLOADS_DIR = "uploads"
OUTPUT_DIR = "templates"

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ✅ Mājaslapas ielāde
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")  # Tagad tiek servēts HTML fails

def process_text(text):
    """ 📌 Pārveido tekstu par SEO draudzīgu un semantiski korektu HTML """
    if not text.strip():
        return "<p>❌ Tukšs saturs! Lūdzu, augšupielādējiet failu ar tekstu.</p>"

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": (
                    "Tu esi AI, kas pārveido tekstu par SEO draudzīgu, semantiski korektu un tīmeklim optimizētu HTML."
                    "Tavi galvenie uzdevumi ir:\n\n"
                    "✅ **Automātiski analizēt un strukturēt tekstu:**\n"
                    "- Atpazīt virsrakstus (H1-H6) un rindkopas.\n"
                    "- Pārveidot sarakstus uz `<ul>` un `<ol>` HTML elementiem.\n"
                    "- Konvertēt tabulas uz `<table>` ar `<thead>`, `<tbody>`, `<th>`, `<td>`.\n"
                    "- Atpazīt programmēšanas kodu un ievietot to `<pre><code>` blokos.\n\n"
                    "✅ **Lasāmība un vizuālais izkārtojums:**\n"
                    "- Nodrošināt skaidru struktūru un pareizu formatējumu.\n"
                    "- Noņemt lieko tekstu un tukšas rindas.\n"
                    "- Izmantot Bootstrap vai pielāgotas CSS klases labākai vizuālajai skaidrībai.\n\n"
                    "✅ **Drošības un validācijas mehānismi:**\n"
                    "- Sanitizēt izvades HTML, lai izvairītos no XSS ievainojamībām.\n"
                    "- Nodrošināt, ka visi speciālie simboli tiek pareizi kodēti (`<`, `>`, `&`, `\"`).\n"
                    "- Saglabāt tikai nepieciešamo informāciju, neizvadot `system` vai `user` metadatus.\n\n"
                    "🔹 **Izvade:** TIKAI validējams un tīrs **HTML kods** (bez liekiem paskaidrojumiem vai teksta)."
                )},
                {"role": "user", "content": text}
            ],
            temperature=0
        )

        return response.choices[0].message.content

    except Exception as e:
        print(f"🚨 Kļūda OpenAI API izsaukumā: {str(e)}")
        return "<p>🚨 Kļūda: Sistēmas kļūme. Mēģiniet vēlreiz!</p>"

@app.route("/upload", methods=["POST"])
def upload_file():
    """ 💄 Augšupielādē un apstrādā tekstu failu """
    try:
        if "file" not in request.files:
            return jsonify({"error": "❌ Nav augšupielādēts fails!"}), 400

        file = request.files["file"]
        if file.filename.strip() == "":
            return jsonify({"error": "❌ Nav izvēlēts fails!"}), 400

        file_path = os.path.join(UPLOADS_DIR, file.filename)
        file.save(file_path)

        # 🔍 Pārbauda, vai fails ir tukšs
        if os.path.getsize(file_path) == 0:
            return jsonify({"error": "❌ Fails ir tukšs!"}), 400

        # 💛 Nolasa failu un apstrādā saturu
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        formatted_content = process_text(content)
        return jsonify({"message": "✅ Fails apstrādāts!", "html_content": formatted_content})

    except Exception as e:
        return jsonify({"error": f"🚨 Servera kļūda: {str(e)}"}), 500

# 🚀 Startē Flask serveri
if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))  # Ja PORT nav iestatīts, izmanto 10000
    app.run(host="0.0.0.0", port=port, debug=True)

