import ctypes
import os
import json
import hashlib
from typing import Optional, Union

from src.colors import col
from src.conf import VAULT_PATH, SECURE_STORAGE_PATH

class User(object):
    def __init__(self):
        self.vault_path = VAULT_PATH
        self.key = ""

        # where to store all file 
        self.vault_storage = SECURE_STORAGE_PATH
        os.makedirs(self.vault_storage, exist_ok=True)

        # the hash of the password
        self.password_manager = self.get_PM()

    def erase_key(self):
        """
        Remove the key from memory and make it unrecoverable
        """

        key_address = id(self.key)
        key_size = len(self.key)
        self._scrub_memory(key_address, key_size)

        # dereference key from memory location
        del self.key
        self.key = b""

    def _scrub_memory(self, address: int, size: int, data: Optional[Union[int, bytes]] = None) -> int:
        """
        Overwrite the memory at the given address with random data.

        if `data` is not none, should be of type int or bytes
        """

        if data is not None:
            assert isinstance(data, (int, bytes)), "data if not None, should be of type int or bytes"

        if data is None:
            data = int.from_bytes(os.urandom(size), byteorder="big")
            size = 1
        elif isinstance(data, bytes):
            data = int.from_bytes(data, byteorder="big")

        return ctypes.memset(address, data, size)



    def get_PM(self, *, verbose: bool = False) -> bytes:
        try:
            with open(self.vault_path, "r") as f:
                file = json.load(f)
                return str(file['PM-hash']).encode()

        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            if verbose:
                if isinstance(e, FileNotFoundError):
                    print(f"{col.YELLOW}file '{self.vault_path}' not found, creating new vault{col.RESET}")
                else:
                    print(f"{col.RED}found currupted file{col.RESET}({e}: {e.msg})")
            return b""

    def validate_key(self, key: str) -> bool:
        key = hashlib.sha512(key.encode()).hexdigest()
        return key == self.password_manager.decode()

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
