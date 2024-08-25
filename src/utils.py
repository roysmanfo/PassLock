import base64
import json

from pathlib import Path
import shlex
from typing import Optional
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

from user import User

def update_vault(user: User, pm_hash: Optional[str] = None, hint: Optional[str] = None, apps: Optional[dict] = None):
    with open(user.vault_path, 'r') as f:
        file = json.load(f)
        
        if pm_hash is None:
            pm_hash: str = file['PM-hash']

        if hint is None:
            hint: str = file['Hint']

        updated_vault = {
            "PM-hash": pm_hash,
            "Hint": hint,
            "Apps": dict(sorted(apps.items())) if apps is not None else file["Apps"] 
        }

    with open(user.vault_path, 'w') as l:
        json.dump(updated_vault, l, indent=4)
        



def compute_key(passw: str, iterations: int = 100_000, key_length: int = 32) -> bytes:
    """
    Uses pbkdf2_hmac to compute the key from the Password Master
    """

    passw = passw.encode()
    salt = b'5df'

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA3_512(),
        length=key_length,
        salt=salt,
        iterations=iterations
    )

    return base64.urlsafe_b64encode(kdf.derive(passw))
    

def path_escape(_files: str) -> list[Path]:
    """
    parse paths, by adding quotes top get the full path and
    returning a list of Path objects

    may trow an exception (from either pathlib or shlex)
    """

    _files: list[str] = shlex.split(shlex.quote(_files))

    files = []
    for file in _files:
        if file.startswith("\"") or file.startswith("'"):
            # this path has been quoted, remove quotes
            file = file[1:-1]
        files.append(Path(file))

    return files


