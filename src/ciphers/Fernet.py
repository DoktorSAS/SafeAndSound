from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import base64

# Define a static salt and IV
STATIC_SALT = b'\x11' * 16
STATIC_IV = b'\x00' * 16  # 16 bytes for AES-128, use 16 bytes regardless of key size for this example

def derive_key_from_text(text: str, salt: bytes = STATIC_SALT) -> bytes:
    """
    Derives a key from the given text using PBKDF2 with SHA256 and a static salt.

    :param text: The text from which to derive the key.
    :param salt: Static salt for key derivation. Default is STATIC_SALT.
    :return: A 32-byte key suitable for AES encryption.
    """
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(text.encode())
    return key

def pad(data: bytes) -> bytes:
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

def unpad(padded_data: bytes) -> bytes:
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data

def encode(data: str, key_text: str) -> str:
    """
    Encrypts the given string data using AES in CBC mode with a static IV.

    :param data: The string data to encrypt.
    :param key_text: The text from which to derive the encryption key.
    :return: The encrypted data as a base64 encoded string.
    """
    key = derive_key_from_text(key_text)
    cipher = Cipher(algorithms.AES(key), modes.CBC(STATIC_IV), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Pad the data
    padded_data = pad(data.encode())
    
    # Encrypt
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Encode to Base64
    return base64.b64encode(ciphertext).decode('utf-8')

def decode(encrypted_data: str, key_text: str) -> str:
    """
    Decrypts the given encrypted string data using AES in CBC mode with a static IV.

    :param encrypted_data: The encrypted string data to decrypt.
    :param key_text: The text from which to derive the decryption key.
    :return: The decrypted data as a string.
    """
    key = derive_key_from_text(key_text)
    cipher = Cipher(algorithms.AES(key), modes.CBC(STATIC_IV), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decode from Base64
    ciphertext = base64.b64decode(encrypted_data)
    
    # Decrypt
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Unpad the data
    data = unpad(padded_data)
    
    return data.decode('utf-8')
