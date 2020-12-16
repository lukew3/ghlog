import configparser
import os
from cryptography.fernet import Fernet
from sys import platform


def get_config_path():
    if platform == "linux" or platform == "linux2":
        config_path = os.path.expanduser("~") + "/.config/ghlog/"
    # darwin is the name for mac os x
    elif platform == "darwin":
        config_path = os.path.expanduser("~") + "/Library/Preferences/ghlog/"
    elif platform == "win32":
        username = os.getlogin()
        config_path = "C:\\Users\\" + username + "\\AppData\\Roaming\\ghlog\\"
    return config_path


def get_config_file():
    config_file = get_config_path() + "config.ini"
    return config_file


def make_empty_config():
    config_file = get_config_file()
    # Checking just in case this was called by accident
    if not os.path.exists(config_file):
        if not os.path.exists(get_config_path()):
            os.makedirs(get_config_path())
        f = open(config_file, 'w')
        f.close()
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'user_token': '',
                         'remote_name': '',
                         'encryption_key': ''}
    with open(config_file, 'w') as configfile:
        config.write(configfile)


def set_token(token):
    config_file = get_config_file()
    if not os.path.exists(config_file):
        os.makedirs(get_config_path())
        f = open(config_file, 'w')
        f.close()
    config = configparser.ConfigParser()
    config.read(get_config_file())
    config['DEFAULT']['user_token'] = token
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    print("token set")


def get_token():
    config = configparser.ConfigParser()
    config.read(get_config_file())
    token = config["DEFAULT"]["user_token"]
    return token


def get_remote_name():
    config = configparser.ConfigParser()
    config.read(get_config_file())
    try:
        remote_name = config["DEFAULT"]["remote_name"]
    except KeyError:
        remote_name = None
    return remote_name


def make_encryption_key():
    config_file = get_config_file()
    key = Fernet.generate_key()
    key_string = key.decode('UTF-8')
    config = configparser.ConfigParser()
    config.read(config_file)
    # Check if encryption key already exists and then ask if the user wants to replace it if it exists
    if config['DEFAULT']['encryption_key'] != '':
        response = input("Encryption key already exists. Replacing it will result in loss of current logs. Would you like to replace it with a new key?(y/n)\n")
        if response == 'y' or response == 'Y':
            print("Replacing key")
        elif response == 'n' or response == 'N':
            print("Keeping current key")
            return None
        else:
            print("Invalid response. Operation aborted.")
            return None
    config['DEFAULT']['encryption_key'] = key_string
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    print("Your encryption key has been stored locally in .config/ghlog/config.ini")


def get_encryption_key():
    config = configparser.ConfigParser()
    config.read(get_config_file())
    key_string = config["DEFAULT"]["encryption_key"]
    if key_string == '':
        return ''
    key = key_string.encode('UTF-8')
    return key


def remove_encryption_key():
    config = configparser.ConfigParser()
    config.read(get_config_file())
    config["DEFAULT"]["encryption_key"] = ''
    with open(get_config_file(), 'w') as configfile:
        config.write(configfile)
