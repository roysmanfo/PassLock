import os
import configparser


def __get_conf__():
    c = configparser.ConfigParser()
    c.read(CONF_PATH)
    return c


# the location of the binary
BIN_PATH = os.path.dirname(os.path.realpath(__file__))

# the location of the vault
VAULT_PATH = os.path.join(os.path.expanduser("~"), ".passlock", "vault.json")

# the location of the secure storage
SECURE_STORAGE_PATH = os.path.join(
    os.path.expanduser("~"), ".passlock", "secure_storage")

# the location of the configuration file
CONF_PATH = os.path.join(BIN_PATH, ".conf")

# the actual configurations as an object (ConfigParser)
CONF = __get_conf__()

# the curent version
VERSION = CONF['general'].get("version", None)
