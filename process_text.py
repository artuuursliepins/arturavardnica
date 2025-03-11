import openai
import os
import json

# 🚀 Ielādē OpenAI API atslēgu no konfigurācijas faila
with open("config.yaml", "r", encoding="utf-8") as f:
    config = json.load(f)
    OPENAI_API_KEY = config["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

# 📂 Augšupielādēto failu direktorija
UPLOADS_DIR = "uploads"
os.makedirs(UPLOADS_DIR, exist_ok=True)

# 📂 Mape, kur tiks saglabāti HTML faili
OUTPUT_DIR = "templates"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_text(file_path):
    """ 📌 Nolasa failu un pārveido tā saturu par HTML izmantojot OpenAI API """
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    # 🔥 OpenAI API pieprasījums
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu esi AI, kas konvertē tekstu par labi formatētu HTML struktūru ar piemērotiem virsrakstiem un rindkopām."},
            {"role": "user", "content": text}
        ]
    )

    # 📜 API atgrieztais HTML saturs
    html_content = response["choices"][0]["message"]["content"]

    return html_content

def convert_all_files():
    """ 📌 Atrod visus tekstu failus un apstrādā tos """
    for file in os.listdir(UPLOADS_DIR):
        file_path = os.path.join(UPLOADS_DIR, file)
        if file.endswith(".txt"):
            print(f"🔄 Apstrādā: {file}")

            # 🚀 Izsauc OpenAI API, lai pārveidotu failu
            html_content = process_text(file_path)

            # 📂 Izveido jaunu HTML failu un saglabā to templates mapē
            output_filename = file.replace(".txt", ".html")
            output_path = os.path.join(OUTPUT_DIR, output_filename)

            with open(output_path, "w", encoding="utf-8") as html_file:
                html_file.write(html_content)

            print(f"✅ Saglabāts: {output_path}")

if __name__ == "__main__":
    convert_all_files()
