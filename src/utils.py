import os, json
from pathlib import Path

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

