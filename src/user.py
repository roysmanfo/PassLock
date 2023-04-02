import os
import json
import hashlib


class User(object):
    def __init__(self):
        self.password_manager = self.get_PM()
        self.key = ""

    def get_PM(self) -> bytes:
        try:
            with open(os.path.join(os.path.dirname(__file__), "data", "vault.json"), "r") as f:
                file = json.load(f)
                return str(file['PM-hash']).encode()

        except FileNotFoundError:
            return b""

        except json.JSONDecodeError:
            return b""

        except KeyError:
            return b""

    def validate_key(self, key: str) -> bool:
        for _ in range(len(key), 32):
            key += "="
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

    def create_vault(self, password):
        os.makedirs(os.path.join(os.path.dirname(
            __file__), "data"), exist_ok=True)
        with open(os.path.join(os.path.dirname(__file__), "data", "vault.json"), "w") as f:
            context = {
                "PM-hash": hashlib.sha512(password.encode()).hexdigest()}
            json.dump(context, f, indent=4, sort_keys=True)
