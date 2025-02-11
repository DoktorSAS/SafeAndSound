from utils.Enum import CryptoType

def encrypt(data: str, cipher: CryptoType, key: str = None) -> str:
    """Encrypt the data using the specified cipher and key."""
    if cipher == CryptoType.AES:
        return "AES encryption not supported"
    elif cipher == CryptoType.RSA:
        return "RSA encryption not supported"
    elif cipher == CryptoType.MD5:
        return "MD5 encryption not supported"
    elif cipher == CryptoType.SHA1:
        return "SHA1 encryption not supported"
    elif cipher == CryptoType.SHA256:
        return "SHA256 encryption not supported"
    elif cipher == CryptoType.SHA512:
        return "SHA512 encryption not supported"
    elif cipher == CryptoType.HMAC:
        return "HMAC encryption not supported"
    elif cipher == CryptoType.ECDSA:
        return "ECDSA encryption not supported"
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
            return "AES decryption not supported"
        elif cipher == CryptoType.RSA:
            return "RSA decryption not supported"
        elif cipher == CryptoType.MD5:
            return "MD5 decryption not supported"
        elif cipher == CryptoType.SHA1:
            return "SHA1 decryption not supported"
        elif cipher == CryptoType.SHA256:
            return "SHA256 decryption not supported"
        elif cipher == CryptoType.SHA512:
            return "SHA512 decryption not supported"
        elif cipher == CryptoType.HMAC:
            return "HMAC decryption not supported"
        elif cipher == CryptoType.ECDSA:
            return "ECDSA decryption not supported"
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
