from enum import Enum

class Browser(Enum):
    CHROMIUM = 0
    FIREFOX = 1
    SAFARI = 2
    EDGE = 3
    IE = 4
    OPERA = 5
    BRAVE = 6
    VIVALDI = 7
    OTHER = 8

class CredentialsType(Enum):
    CREDENTIALS = 0
    PLAINTEXT = 1

class CryptoType(Enum):
    AES = "AES"
    FERNET = "FERNET"
    BASE64 = "BASE64"
    NONE = "NONE"

    @staticmethod
    def string_to_enum(value: str):
        for item in CryptoType:
            if item.value == value:
                return item
        return None
