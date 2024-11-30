from typing import Tuple  
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os
from pathlib import Path
import logging

def encrypt_document_aes(file_path: Path, key: bytes) -> bytes:
    try:
        iv = os.urandom(16)  

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        with open(file_path, 'rb') as f:
            document_data = f.read()

        padding_length = 16 - len(document_data) % 16
        document_data += bytes([padding_length]) * padding_length  

        encrypted_data = encryptor.update(document_data) + encryptor.finalize()

        return iv + encrypted_data

    except Exception as e:
        logging.error(f"Error encrypting document with AES: {e}")
        raise Exception("Error encrypting the document with AES")

async def save_document_to_media(file_data: bytes, file_name: str) -> Path:
    try:
        media_folder = Path('media')
        media_folder.mkdir(parents=True, exist_ok=True)

        file_path = media_folder / file_name
        with open(file_path, 'wb') as f:
            f.write(file_data)
        return file_path

    except Exception as e:
        logging.error(f"Error saving document: {e}")
        raise Exception("Error saving the document to media folder")

async def handle_upload_and_encrypt(document_data: bytes, file_name: str, encryption_key: bytes) -> Tuple[Path, bytes]:
    try:

        file_path = await save_document_to_media(document_data, file_name)

        encrypted_data = encrypt_document_aes(file_path, encryption_key)

        return file_path, encrypted_data

    except Exception as e:
        logging.error(f"Error during document upload and encryption: {e}")
        raise Exception("Error during document upload and encryption")


def decrypt_document_aes(file_path: Path, key: bytes) -> bytes:
    try:
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()

        iv = encrypted_data[:16]
        encrypted_data = encrypted_data[16:] 

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

        padding_length = decrypted_data[-1]
        return decrypted_data[:-padding_length]  

    except Exception as e:
        logging.error(f"Error decrypting document: {e}")
        raise Exception("Error decrypting the document")
