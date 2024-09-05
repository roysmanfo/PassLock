import os
import configparser


def _get_conf():
    c = configparser.ConfigParser()
    c.read(CONF_PATH)
    return c


# the location of the binary
BIN_PATH = os.path.dirname(os.path.realpath(__file__))

# the location of the vault
VAULT_PATH = os.path.join(os.path.expanduser("~"),
                          ".passlock", "vault.sqlite3")

# the location of the configuration file
CONF_PATH = os.path.join(BIN_PATH, ".conf")

# the actual configurations as an object (ConfigParser)
CONF = _get_conf()

# the curent version
VERSION = CONF['general'].get("version", None)
