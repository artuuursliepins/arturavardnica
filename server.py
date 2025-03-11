!pip install flask pyngrok

from flask import Flask, request, render_template_string, redirect, url_for, session
from pyngrok import ngrok
import threading
import os

# 🔐 Lietotājvārds un parole
USERNAME = "artuuursliepins"
PASSWORD = "I*3pieci9212667"

# 🔑 Ngrok autentifikācijas atslēga
NGROK_AUTH_TOKEN = "2u9CrT77rLsHfhxmVFgcp25h8j9_yVESnV1qvoyhQ6bmXxPc"
ngrok.set_auth_token(NGROK_AUTH_TOKEN)

# 🚀 Flask aplikācijas inicializācija
app = Flask(__name__)
app.secret_key = "super_secret_key"  # Sesijas drošībai

# 📂 Nodrošinām, ka augšupielādes mape eksistē
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🌐 Mājaslapa ar autentifikāciju
@app.route("/")
def home():
    if "logged_in" in session and session["logged_in"]:
        return """<h1>Matemātisko Simbolu Vārdnīca</h1>
                  <p>Šeit varēsi augšupielādēt failus!</p>
                  <form action="/upload" method="post" enctype="multipart/form-data">
                      <input type="file" name="file">
                      <input type="submit" value="📤 Augšupielādēt">
                  </form>
                  <br>
                  <a href='/logout'>🚪 Iziet</a>"""
    return redirect(url_for("login"))

# 🔐 Autentifikācija
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == USERNAME and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            return "❌ Nepareizs lietotājvārds vai parole! <a href='/login'>Mēģini vēlreiz</a>"

    return """<h2>Pieslēgties</h2>
              <form method="post">
                  Lietotājvārds: <input type="text" name="username"><br>
                  Parole: <input type="password" name="password"><br>
                  <input type="submit" value="Pieslēgties">
              </form>"""

# 🚪 Izrakstīšanās
@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))

# 📤 Failu augšupielāde (pieejama tikai autentificētiem lietotājiem)
@app.route("/upload", methods=["POST"])
def upload_file():
    if "logged_in" not in session or not session["logged_in"]:
        return "❌ Jums nav atļaujas piekļūt šai lapai!", 403

    file = request.files["file"]
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return f"✅ Fails saglabāts: {file_path}", 200

# 🔄 Flask servera palaišana fonā ar portu 5001
def run():
    app.run(host="0.0.0.0", port=5001)

thread = threading.Thread(target=run)
thread.start()

# 🌍 Ngrok publiskās saites izveide uz portu 5001
public_url = ngrok.connect(5001).public_url
print(f"🚀 Ngrok publiskā saite: {public_url}")
