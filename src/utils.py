import base64
import json
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

from user import User

def update_vault(user: User, pm_hash: str = None, hint: str = None, apps: dict = None):
    with open(user.vault_path, 'r') as f:
        file = json.load(f)
        pm_hash: str = file['PM-hash'] if pm_hash is None else pm_hash
        updated_vault = {
            "PM-hash": pm_hash if pm_hash is None else file['PM-hash'],
            "Hint": hint if hint is not None else file['Hint'],
            "Apps": dict(sorted(apps.items())) if apps is not None else file["Apps"] 
        }

    with open(user.vault_path, 'w') as l:
        json.dump(updated_vault, l, indent=4)
        



def compute_key(passw: str, iterations: int = 100_000, key_length: int = 32, salt: str = b"5df") -> bytes:
    """
    Uses pbkdf2_hmac to compute the key from the Password Master
    """

    passw = passw.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_512(),
        length=key_length,
        salt=salt,
        iterations=iterations
    )

    return base64.urlsafe_b64encode(kdf.derive(passw))
    

