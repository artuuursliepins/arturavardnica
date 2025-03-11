import os
import openai
from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  # ✅ PIEVIENO CORS ATBALSTU
from flask_cors import CORS
CORS(app)

# 🚀 Ielādē API atslēgu no Render Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ Kļūda: OpenAI API atslēga nav atrasta Render platformā!")

openai.api_key = OPENAI_API_KEY
print("API Response:", response)

app = Flask(__name__)
CORS(app)  # ✅ PIEVIENO CORS, LAI ATĻAUTU FETCH PIEPRASĪJUMUS NO PĀRLŪKA

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🌍 Mājaslapa
@app.route("/")
def home():
    return render_template("index.html")

# 📤 Failu augšupielāde un apstrāde
@app.route("/upload", methods=["POST"])
def upload_file():
    print("📥 Saņemts pieprasījums uz /upload")  # ✅ DEBUG: PĀRBAUDI, VAI PIEPRASĪJUMS NONĀK SERVERĪ

    if "file" not in request.files:
        print("❌ Nav augšupielādēts fails!")  # ✅ DEBUG LOG
        return jsonify({"error": "❌ Nav augšupielādēts fails!"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        print("❌ Nav izvēlēts fails!")  # ✅ DEBUG LOG
        return jsonify({"error": "❌ Nav izvēlēts fails!"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    print(f"✅ Fails saglabāts: {file_path}")  # ✅ DEBUG LOG

    # 🚀 Pārveido saturu ar OpenAI API
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    formatted_content = convert_text_to_html(content)
    
    return jsonify({"message": "✅ Fails apstrādāts!", "html_content": formatted_content})

# 🔥 OpenAI API Teksta Pārveidošana
def convert_text_to_html(text):
    response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "Formātējiet šo tekstu kā HTML dokumentu."},
        {"role": "user", "content": text}
    ],
    temperature=0,  # Nodrošina precīzākas atbildes
  
)
    return response["choices"][0]["message"]["content"]

print("API Response:", response)

# 🚀 Startē Flask Serveri
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
