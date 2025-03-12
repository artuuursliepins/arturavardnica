import os
import openai

# 🚀 Ielādē OpenAI API atslēgu no Render Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ Kļūda: OpenAI API atslēga nav atrasta Render vidē!")

# ✅ Pareiza OpenAI API inicializācija
openai.api_key = OPENAI_API_KEY

def process_text(text):
    """ 📌 Sastrukturizē un optimizē tekstu par HTML, izmantojot GPT-4o """

    if not text.strip():
        return "<p>❌ Tukšs saturs! Lūdzu, augšupielādējiet failu ar tekstu.</p>"

    try:
        response = openai.ChatCompletion.create(
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

        return response["choices"][0]["message"]["content"]

    except openai.OpenAIError as e:
        print(f"❌ OpenAI API kļūda: {str(e)}")
        return "<p>❌ Kļūda, apstrādājot tekstu ar OpenAI.</p>"

    except Exception as e:
        print(f"🚨 Nezināma kļūda: {str(e)}")
        return "<p>🚨 Kļūda: Sistēmas kļūme. Mēģiniet vēlreiz!</p>"