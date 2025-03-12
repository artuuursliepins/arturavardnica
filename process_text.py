import os
from openai import OpenAI
import html

# 🚀 Ielādē OpenAI API atslēgu no Render Environment Variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("❌ Kļūda: OpenAI API atslēga nav atrasta Render vidē!")

# ✅ OpenAI API inicializācija
client = OpenAI()

def process_text(text):
    """ 📌 Sastrukturizē un optimizē tekstu par HTML, izmantojot GPT-4o """

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

        html_output = response.choices[0].message.content

        # ✅ Sanitizē HTML izvadi, lai novērstu XSS ievainojamības
        safe_html_output = html.escape(html_output)

        return safe_html_output

    except Exception as e:
        print(f"🚨 Kļūda OpenAI API izsaukumā: {str(e)}")
        return f"<p>🚨 Kļūda: {html.escape(str(e))}</p>"