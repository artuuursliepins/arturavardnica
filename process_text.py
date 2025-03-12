import os
import openai
import yaml
from flask import Flask, request, jsonify

# 🚀 Ielādē OpenAI API atslēgu no konfigurācijas faila
CONFIG_FILE = "config.yaml"
if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError("❌ Kļūda: Konfigurācijas fails 'config.yaml' nav atrasts!")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
    OPENAI_API_KEY = config.get("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ Kļūda: OpenAI API atslēga nav norādīta konfigurācijas failā!")

# ✅ OpenAI API inicializācija
openai.api_key = OPENAI_API_KEY

# 📂 Direktorijas failiem
UPLOADS_DIR = "uploads"
OUTPUT_DIR = "templates"

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_text(text):
    """ 📌 Sastrukturizē un optimizē tekstu par HTML, izmantojot GPT-4o """
    if not text.strip():
        return "<p>❌ Tukšs saturs! Lūdzu, augšupielādējiet failu ar tekstu.</p>"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": (
                    "Tu esi AI, kas pārveido vienkāršu tekstu par SEO draudzīgu, semantiski korektu un responsīvu HTML. "
                    "Tavi galvenie uzdevumi ir:\n\n"
                    "✅ Automātiski identificēt un strukturēt saturu:\n"
                    "  - Noteikt virsrakstus (H1-H6), rindkopas, sarakstus, tabulas un kodu blokus.\n"
                    "  - Nodrošināt loģisku rindkopu dalījumu un izvairīties no liekām atstarpēm.\n"
                    "  - Pievienot Bootstrap vai pielāgotas CSS klases, lai nodrošinātu vizuāli pievilcīgu attēlojumu.\n\n"
                    "✅ Speciālo rakstzīmju aizvietošana:\n"
                    "  - Korekti apstrādāt <, >, &, \" un citus HTML simbolus, lai nodrošinātu drošību.\n\n"
                    "✅ Inteliģenta tabulu un koda formatēšana:\n"
                    "  - Konvertēt tabulveida datus par <table> struktūru ar korektiem <thead>, <tbody>, <th>, <td> elementiem.\n"
                    "  - Atpazīt programmēšanas kodu un ievietot to <pre><code> blokos ar atbilstošu sintakses izcelšanu (piemēram, Prism.js).\n\n"
                    "✅ Drošības un validācijas mehānismi:\n"
                    "  - Nodrošināt, ka HTML kods ir validējams pēc W3C standartiem.\n"
                    "  - Novērst XSS ievainojamības, izvairoties no nevajadzīgiem inline skriptiem.\n\n"
                    "🔹 Izvade: TIKAI tīrs un semantiski korekts HTML, piemērots tūlītējai lietošanai tīmeklī."
                )},
                {"role": "user", "content": text}
            ],
            temperature=0
        )

        return response["choices"][0]["message"]["content"]

    except openai.error.OpenAIError as e:
        print(f"❌ OpenAI API kļūda: {str(e)}")
        return "<p>❌ Kļūda, apstrādājot tekstu ar OpenAI.</p>"

def convert_all_files():
    """ 📌 Apstrādā visus .txt failus un saglabā strukturētu HTML """
    for file in os.listdir(UPLOADS_DIR):
        file_path = os.path.join(UPLOADS_DIR, file)

        if file.endswith(".txt") and os.path.isfile(file_path):
            print(f"🔄 Apstrādā: {file}")

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                if not text.strip():
                    print(f"⚠️ Tukšs fails: {file}")
                    continue

                # 🚀 Pārveido tekstu uz HTML
                html_content = process_text(text)

                # 📂 Saglabā kā HTML failu
                output_filename = file.replace(".txt", ".html")
                output_path = os.path.join(OUTPUT_DIR, output_filename)

                with open(output_path, "w", encoding="utf-8") as html_file:
                    html_file.write(html_content)

                print(f"✅ Saglabāts: {output_path}")

            except Exception as e:
                print(f"❌ Kļūda apstrādājot failu {file}: {str(e)}")

# 🌍 Flask API
app = Flask(__name__)

@app.route("/upload", methods=["POST"])
def upload_file():
    """ 📤 Augšupielādē un apstrādā tekstu failu """
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

        # 📜 Nolasa failu un apstrādā saturu
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        formatted_content = process_text(content)
        return jsonify({"message": "✅ Fails apstrādāts!", "html_content": formatted_content})

    except Exception as e:
        return jsonify({"error": f"🚨 Servera kļūda: {str(e)}"}), 500

# 🚀 Startē Flask serveri
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)