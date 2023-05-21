import base64
import os, json
from pathlib import Path
from hashlib import pbkdf2_hmac
from cryptography.hazmat.primitives import hashes

def update_vault(apps: dict, vault_path: str | Path):
    with open(vault_path, 'r') as f:
        file = json.load(f)
        pm_hash: str = file['PM-hash']
        updated_vault = {
            "PM-hash": pm_hash,
            "Apps": dict(sorted(apps.items()))
        }
        with open(os.path.join('data', 'vault.json'), 'w') as l:
            json.dump(updated_vault, l, indent=4)


def compute_key(passw: str, iterations: int = 100_000, key_length: int = 32) -> bytes:
    """
    Uses pbkdf2_hmac to compute the key from the Password Master
    """

    passw.encode()
    salt = b'5df'

    kdf = pbkdf2_hmac(
        algorithm=hashes.SHA3_512(),
        length=key_length,
        salt=salt,
        iterations=iterations
    )
    key = base64.urlsafe_b64encode(kdf.derive(passw))
    return key

