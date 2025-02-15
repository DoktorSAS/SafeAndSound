from utils.Enum import CryptoType

from ciphers.AES import derive_key_from_data as AES_Derive_Key 
from ciphers.Fernet import derive_key_from_text as Fernet_derive_key_from_text

def encrypt(data: str, cipher: CryptoType, key: str = None) -> str:
    """Encrypt the data using the specified cipher and key."""
    if cipher == CryptoType.AES:
        from ciphers.AES import encode as AES_encode
        if key is None or key == "":
            key = AES_Derive_Key(data)
       
        byte_data = data.encode('utf-8')
        ciphertext, nonce, tag = AES_encode(key, byte_data)
        combined = nonce + tag + ciphertext
        return encrypt(str(combined), CryptoType.BASE64)
    if cipher == CryptoType.FERNET:
        from ciphers.Fernet import encode as Fernet_encode
        if key is None or key == "":
            key = data
        return Fernet_encode(data, key)
    elif cipher == CryptoType.BASE64:
        from ciphers.Base64 import encode as Base64_encode
        str_data = Base64_encode(data.encode('utf-8')).decode('utf-8')
        return str_data
    else:
        return data
    pass
    
def decrypt(data: str, cipher: CryptoType, key: str = "") -> str:
    """Decrypt the data using the specified cipher and key."""
    try:
        if cipher == CryptoType.AES:
            print ("\n",data)
            decoded_data = decrypt(data, CryptoType.BASE64)
       
            nonce = decoded_data[:16].encode('utf-8')
            tag = decoded_data[16:32].encode('utf-8')
            ciphertext = decoded_data[32:].encode('utf-8')
            
            from ciphers.AES import decode as AES_decode
            
            # Decrypt the AES data
            decrypted_data = AES_decode(key, nonce, tag, ciphertext)
            return decrypted_data.decode('utf-8')
        if cipher == CryptoType.FERNET:
            from ciphers.Fernet import decode as Fernet_decode
            if key is None or key == "":
                key = data
            return Fernet_decode(data, key)
        elif cipher == CryptoType.BASE64:
            from ciphers.Base64 import decode as Base64_decode
            byte_data = Base64_decode(data.encode('utf-8')).decode('utf-8')
            return str(byte_data)
        else:
            from ciphers.Base64 import encode as Base64_encode
            return Base64_encode(data[:-2].encode('utf-8')).decode('utf-8')[:-2]
    except:
        from ciphers.Base64 import encode as Base64_encode
        return Base64_encode(data[:-2].encode('utf-8')).decode('utf-8')[:-2]
