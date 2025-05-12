from flask import Flask, render_template, request, redirect, url_for
import os, json
from decrypt_photo import decrypt_photo

app = Flask(__name__)
LOCKED_DIR = "fotos_bloqueadas"
UNLOCKED_DIR = os.path.join("static", "fotos")
PROGRESS_FILE = "progresso.json"

os.makedirs(UNLOCKED_DIR, exist_ok=True)

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f)

@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    unlocked = load_progress()
    total_photos = sorted([f for f in os.listdir(LOCKED_DIR) if f.endswith(".enc")])

    if request.method == "POST":
        chave = request.form.get("chave").strip().encode()
        for nome in total_photos:
            num = nome[:2]
            if num in unlocked:
                continue
            path_enc = os.path.join(LOCKED_DIR, nome)
            try:
                data = decrypt_photo(path_enc, chave)
                output_path = os.path.join(UNLOCKED_DIR, f"{num}.jpg")
                with open(output_path, 'wb') as out:
                    out.write(data)
                unlocked.append(num)
                save_progress(unlocked)
                message = f"✅ Foto {num} desbloqueada com sucesso!"
                break
            except Exception:
                continue
        else:
            message = "❌ Nenhuma foto foi desbloqueada com essa chave."

    photos = []
    for nome in total_photos:
        num = nome[:2]
        if num in unlocked:
            url = url_for('static', filename=f"fotos/{num}.jpg")
        else:
            url = url_for('static', filename="locked.jpg")
        photos.append((num, url))

    return render_template("index.html", photos=photos, message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
