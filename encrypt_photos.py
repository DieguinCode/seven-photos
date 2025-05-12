import os
from cryptography.fernet import Fernet

INPUT_DIR = "fotos_original"
OUTPUT_DIR = "fotos_bloqueadas"
KEYS_DIR = "keys"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(KEYS_DIR, exist_ok=True)

photos = sorted([f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])

for i, photo_name in enumerate(photos, 1):
    photo_path = os.path.join(INPUT_DIR, photo_name)
    key = Fernet.generate_key()
    fernet = Fernet(key)

    with open(photo_path, 'rb') as file:
        data = file.read()

    encrypted = fernet.encrypt(data)

    with open(os.path.join(OUTPUT_DIR, f"{i:02d}.enc"), 'wb') as file:
        file.write(encrypted)

    with open(os.path.join(KEYS_DIR, f"{i:02d}.key"), 'wb') as file:
        file.write(key)

    print(f"[OK] Foto {photo_name} criptografada como {i:02d}.enc")
