import os

from dotenv import find_dotenv, load_dotenv
from cryptography.fernet import Fernet

load_dotenv(find_dotenv())

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables!")

cipher = Fernet(SECRET_KEY.encode())

def encrypt_data(data: str) -> bytes:
    """Шифрует данные"""
    return cipher.encrypt(data.encode())

def decrypt_data(encrypted_data: str) -> bytes:
    """Расшифровывает данные"""
    return cipher.decrypt(encrypted_data.encode())