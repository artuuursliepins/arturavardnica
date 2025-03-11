@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        if "file" not in request.files:
            return jsonify({"error": "❌ Nav augšupielādēts fails!"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "❌ Nav izvēlēts fails!"}), 400

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # 🔍 Pārbauda, vai fails eksistē
        if not os.path.exists(file_path):
            return jsonify({"error": "❌ Fails netika saglabāts pareizi!"}), 500

        # 📜 Mēģina apstrādāt faila saturu ar OpenAI API
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            formatted_content = convert_text_to_html(content)
            return jsonify({"message": "✅ Fails apstrādāts!", "html_content": formatted_content})
        
        except Exception as e:
            return jsonify({"error": f"❌ Kļūda apstrādājot failu: {str(e)}"}), 500

    except Exception as e:
        return jsonify({"error": f"🚨 Servera kļūda: {str(e)}"}), 500