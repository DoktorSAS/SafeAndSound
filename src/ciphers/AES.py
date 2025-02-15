from Crypto.Cipher import AES
from Crypto.Hash import HMAC, SHA256
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256

def encode_with_fixed_nonce(key: bytes, data: bytes, nonce: bytes = None) -> tuple:
    """
    Encrypts data using AES in EAX mode with an optional fixed nonce for testing.

    :param key: The encryption key, must be 16, 24, or 32 bytes long for AES-128, AES-192, or AES-256 respectively.
    :param data: The data to encrypt, provided as bytes.
    :param nonce: Optional fixed nonce for testing. If not provided, a new nonce will be generated.
    :return: A tuple containing (ciphertext, nonce, tag) where:
             - ciphertext: The encrypted data.
             - nonce: The nonce used for this encryption operation.
             - tag: The authentication tag for integrity verification.
    """
    if nonce is None:
        nonce = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, nonce, tag

def decode(key: bytes, nonce: bytes, tag: bytes, data: bytes) -> bytes:
    """
    Decrypts data encrypted with AES in EAX mode.

    :param key: The decryption key, must match the key used for encryption.
    :param nonce: The nonce used during encryption, must be provided to decrypt correctly.
    :param tag: The authentication tag from the encryption process, used for integrity check.
    :param data: The encrypted data (ciphertext) to decrypt, provided as bytes.
    :return: The decrypted data as bytes.
    :raises ValueError: If the decryption fails or the tag does not match.
    """
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(data, tag)
    
def derive_key_from_data(data: str, key_length: int = 32) -> str:
    """
    Derives a key from the given data using SHA-256, with the option to specify the key length.

    :param data: The input data from which to derive the key, provided as a string.
    :param key_length: The desired length of the key in bytes. Default is 32 (for AES-256).
    :return: A key derived from the input data, truncated or extended to the specified length.

    **Note**: This method is deterministic and should not be used for generating keys 
    for cryptographic purposes where true randomness is required. Also, ensure key_length 
    is not greater than the hash output size (32 bytes for SHA-256).
    """
    # Convert the data string to bytes
    data_bytes = data.encode('utf-8')
    
    # Use SHA-256 to hash the data
    hash_object = SHA256.new(data_bytes)
    
    # Get the digest of the hash
    full_key = hash_object.digest()
    
    # If the requested key length is less than or equal to the hash length, truncate
    if key_length <= len(full_key):
        return full_key[:key_length]
    else:
        # If the key length is greater than the hash length, we'll repeat the hash
        # This is not recommended for real-world cryptographic use due to security concerns
        extended_key = full_key
        while len(extended_key) < key_length:
            hash_object = SHA256.new(extended_key + data_bytes)
            extended_key += hash_object.digest()
        return extended_key[:key_length].decode('utf-8')
    
def encode(key: bytes, data: bytes) -> tuple:
    """
    Encrypts data using AES in EAX mode.

    :param key: The encryption key, must be 16, 24, or 32 bytes long for AES-128, AES-192, or AES-256 respectively.
    :param data: The data to encrypt, provided as bytes.
    :return: A tuple containing (ciphertext, nonce, tag) where:
             - ciphertext: The encrypted data.
             - nonce: The nonce used for this encryption operation.
             - tag: The authentication tag for integrity verification.
    """
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    return ciphertext, cipher.nonce, tag

def decode(key: bytes, nonce: bytes, tag: bytes, data: bytes) -> bytes:
    """
    Decrypts data encrypted with AES in EAX mode.

    :param key: The decryption key, must match the key used for encryption.
    :param nonce: The nonce used during encryption, must be provided to decrypt correctly.
    :param tag: The authentication tag from the encryption process, used for integrity check.
    :param data: The encrypted data (ciphertext) to decrypt, provided as bytes.
    :return: The decrypted data as bytes.
    :raises ValueError: If the decryption fails or the tag does not match.
    """
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(data, tag)

# Example usage
"""
Example of usage:

# Generate a 256-bit key for AES-256 (32 bytes)
key = get_random_bytes(32)

# Data to encrypt
data = b"Hello, this is a secret message"

# Encrypt the data
ciphertext, nonce, tag = encode(key, data)

print(f"Encrypted data: {ciphertext}")
print(f"Nonce: {nonce}")
print(f"Tag: {tag}")

# Decrypt the data
decrypted_data = decode(key, nonce, tag, ciphertext)

print(f"Decrypted data: {decrypted_data.decode('utf-8')}")
"""

# Example usage
"""
Example of usage:

# Derive a key from a passphrase or any data string
data = "This is my secret passphrase"
key = derive_key_from_data(data)

# Data to encrypt
data_to_encrypt = b"Hello, this is a secret message"

# Encrypt the data
ciphertext, nonce, tag = encode(key, data_to_encrypt)

print(f"Encrypted data: {ciphertext}")
print(f"Nonce: {nonce}")
print(f"Tag: {tag}")

# Decrypt the data
decrypted_data = decode(key, nonce, tag, ciphertext)

print(f"Decrypted data: {decrypted_data.decode('utf-8')}")
"""