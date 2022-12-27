"""
This module handles encoding and decoding of a string
"""

from cryptography.fernet import Fernet

class Secure():
    def __init__(self, key: str = ""):
        self.key = key
        
        if key == "":
            self.key = Fernet.generate_key()
        
        self.fernet = Fernet(key)

    def encrypt(self, data: str):
        return self.fernet.encrypt(bytes(data))
    
    def decrypt(self, data: str):
        return self.fernet.decrypt(bytes(data))
