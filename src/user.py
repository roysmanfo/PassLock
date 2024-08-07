import os
import json
import hashlib


class User(object):
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.key = ""
        self.password_manager = self.get_PM()

    def get_PM(self) -> bytes:
        try:
            with open(self.vault_path, "r") as f:
                file = json.load(f)
                return str(file['PM-hash']).encode()

        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return b""

    def validate_key(self, key: str) -> bool:
        key = hashlib.sha512(key.encode()).hexdigest()
        return True if key == self.password_manager.decode() else False

    def check_password(self, passw: str) -> bool:
        """
        Checks if the Password Master satisfies the minimum password requirements

        - min length : 8
        - all uppercase letters: False
        - all lowercase letters: False
        - min uppercase letters: 1
        """

        if len(passw) < 8:
            return False

        if passw.upper() == passw or passw.lower() == passw:
            return False

        return True

    def create_vault(self, password: str, hint: str):            
        os.makedirs(self.vault_path.removesuffix("vault.json"), exist_ok=True)
        with open(self.vault_path, "w") as f:
            context = {
                "PM-hash": hashlib.sha512(password.encode()).hexdigest(),
                "Hint": hint,
                "Apps": {}
                }
            json.dump(context, f, indent=4)
