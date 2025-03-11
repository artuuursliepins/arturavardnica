from flask import Flask, request, render_template, redirect, url_for, session
from pyngrok import ngrok
import os
import json
import openai

# 🔑 Ielādē OpenAI API atslēgu
with open("config.yaml", "r") as f:
    config = json.load(f)
    OPENAI_API_KEY = config["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

app = Flask(__name__)
app.secret_key = "super_secret_key"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return redirect(url_for("home"))

if __name__ == "__main__":
    public_url = ngrok.connect(10000).public_url
    print(f"🚀 Ngrok publiskā saite: {public_url}")
    app.run(host="0.0.0.0", port=10000)

