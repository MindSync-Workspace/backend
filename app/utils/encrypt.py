import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import logging
import base64


def encrypt_document_aes(file_data: bytes, key: bytes) -> bytes:
    try:
        iv = os.urandom(16)  # Generate a random IV

        # Create AES cipher object in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()

        # Add padding to the document data to be a multiple of block size (16 bytes)
        padding_length = 16 - len(file_data) % 16
        file_data += bytes([padding_length]) * padding_length  # Pad with the length of the padding

        encrypted_data = encryptor.update(file_data) + encryptor.finalize()

        return iv + encrypted_data  # Prepend IV to the encrypted data for decryption

    except Exception as e:
        logging.error(f"Error encrypting document with AES: {e}")
        raise Exception("Error encrypting the document with AES")
    
def decrypt_document_aes(encrypted_data: bytes, key_base64: str) -> bytes:
    try:
        # Decode the base64-encoded key back to bytes
        key = base64.b64decode(key_base64)

        if len(key) != 32:
            raise Exception("Invalid encryption key size, must be 32 bytes for AES-256")

        iv = encrypted_data[:16]  # The first 16 bytes are the IV
        cipher_data = encrypted_data[16:]  # The rest is the encrypted document data

        # Create AES cipher object in CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()

        decrypted_data = decryptor.update(cipher_data) + decryptor.finalize()

        # Remove padding (16 bytes) from the decrypted document
        padding_length = decrypted_data[-1]
        return decrypted_data[:-padding_length]  # Remove padding

    except Exception as e:
        logging.error(f"Error decrypting document with AES: {e}")
        raise Exception("Error decrypting the document with AES")