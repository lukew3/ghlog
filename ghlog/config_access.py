import configparser
import os


def set_token(token):
    config_file = os.path.expanduser("~") + "/.config/ghlog/config.ini"
    if not os.path.exists(config_file):
        os.makedirs(os.path.expanduser("~") + "/.config/ghlog")
        f = open(config_file, 'w')
        f.close()
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'user_token': token}
    with open(config_file, 'w') as configfile:
        config.write(configfile)
    print("token set")


def get_token():
    config_file = os.path.expanduser("~") + "/.config/ghlog/config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
    token = config["DEFAULT"]["user_token"]
    return token


def get_remote_name():
    config_file = os.path.expanduser("~") + "/.config/ghlog/config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
    try:
        remote_name = config["DEFAULT"]["remote_name"]
    except KeyError:
        remote_name = None
    return remote_name
