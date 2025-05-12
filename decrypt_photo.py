from cryptography.fernet import Fernet

def decrypt_photo(photo_path: str, key: bytes) -> bytes:
    with open(photo_path, 'rb') as file:
        encrypted = file.read()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted)
