# imagenc_v2.py

import base64
import os
import hashlib
import random
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def generate_key_from_image(image_data):
    """
    Generates a deterministic but random-looking key from image data.
    """
    if not image_data:
        raise ValueError("Image data cannot be empty.")
    
    # 1. Hash the entire image data to get a seed.
    img_hash = hashlib.sha256(image_data).digest()
    
    # 2. Use the hash as a seed for the random number generator.
    # This ensures the "random" starting point is the same for the same image.
    random.seed(img_hash)
    
    # 3. Base64 encode the image data.
    b64_data = base64.b64encode(image_data)
    
    # We need at least 32 bytes to create a key.
    if len(b64_data) < 32:
        raise ValueError("Image is too small to generate a secure key.")
        
    # 4. Choose a random starting point to slice 32 bytes from.
    max_start_index = len(b64_data) - 32
    start_index = random.randint(0, max_start_index)
    
    return b64_data[start_index : start_index + 32]

def encrypt_password(password, key):
    """
    Encrypts the password using AES-256-CBC.
    """
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    # Pad password to be a multiple of 16
    padded_password = password.encode() + (16 - len(password.encode()) % 16) * b'\0'
    encrypted_password = encryptor.update(padded_password) + encryptor.finalize()
    return base64.b64encode(iv + encrypted_password)

def decrypt_password(encrypted_password_b64, key):
    """
    Decrypts the password.
    """
    encrypted_password = base64.b64decode(encrypted_password_b64)
    iv = encrypted_password[:16]
    encrypted_data = encrypted_password[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_password_padded = decryptor.update(encrypted_data) + decryptor.finalize()
    # Unpad by removing null bytes
    return decrypted_password_padded.rstrip(b'\0').decode()