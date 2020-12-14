import click
import os
import configparser
from github import Github
from datetime import datetime
from .config_access import set_token, get_token, get_remote_name, make_encryption_key, get_encryption_key
import time
from multiprocessing.pool import ThreadPool
from cryptography.fernet import Fernet


@click.command()
@click.option('-t', '--set-token', 'token', help='Set Github personal access token.')
@click.option('-r', '--create-repo', 'new_repo_name', help='Create new Github repo with passed name.')
@click.option('-f', '--fetch-logs', 'date', help='Get log entries from a certain date, month, or year. Use (yyyy/mm/dd) and stop after your desired time. Ex: 2020/12 for December 2020, 2019/08/15 for August 15th 2019')
@click.option('-m', '--make-readme', help='Combines all logs into the Github README', is_flag=True)
@click.option('-e', '--encrypt', help='Encrypt your logs from now on. Warning: your logs will not be readable on Github, they must be decrypted locally to be readable.', is_flag=True)
def cli(token, new_repo_name, date, make_readme, encrypt):
    """ A minimal command-line journal that saves to a Github repo """
    if token is not None:
        set_token(token)
        return None

    if new_repo_name is not None:
        create_repo(repo_name=new_repo_name)
        return None

    if date is not None:
        print(get_logs_by_date(date))
        return None

    if make_readme:
        make_readme_md()
        return None

    if encrypt:
        make_encryption_key()
        return None

    config_file = os.path.expanduser("~") + "/.config/ghlog/config.ini"
    # This doesn't work if token was deleted from file, which is unlikely but still possible
    if not os.path.exists(config_file):
        print("No personal access token added. To set token, user 'ghlog -t <token>'")
        print("Get help setting up at https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token. Only repo permission is necessary.")
        return None

    add_entry()


def get_logs_by_date(datestring):
    output_lines = []
    output = ""
    token = get_token()
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(get_remote_name())
    try:
        contents = repo.get_contents("entries/" + datestring)
        # This could be reused to work for year and month spaces of time
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                log_contents = file_content.decoded_content.decode()
                if get_encryption_key() is not None:
                    log_contents = decrypt_text(log_contents)
                output_lines.append(log_contents)
        output = '\n'.join(output_lines)
    except Exception:
        output = "No entries found for specified day(s)"
    return output


def create_repo(repo_name="My-Log"):
    token = get_token()
    g = Github(token)
    user = g.get_user()
    repos = user.get_repos()
    for repo in repos:
        if repo.name == repo_name:
            print("Repo with name '" + repo_name + "' already exists. Delete it or choose a different name.")
            return None
    print("Creating Github repo...")
    repo = user.create_repo(repo_name, private=True)
    # Add README.md with title to github
    titlebar = '=' * len(repo_name)
    content = repo_name + '\n' + titlebar + '\n'
    repo.create_file("README.md", "initial commit", content, branch="main")
    # Write repo name to config
    config_file = os.path.expanduser("~") + "/.config/ghlog/config.ini"
    config = configparser.ConfigParser()
    config.read(config_file)
    config["DEFAULT"]["remote_name"] = repo_name
    with open(config_file, 'w') as configfile:
        config.write(configfile)


def add_entry():
    # Check if repo exists, if not create it
    # This method doesn't work if the user deleted their remote but kept their config file
    if get_remote_name() is None:
        # Ask what the user would like to call their repo before creating it; default to My-ghlog
        create_repo()

    entry = input("Write your entry: ")
    if entry == "":
        print("Entry discarded")
        return None
    now = datetime.now()
    contents = entry + '\n'
    message = now.strftime("%m/%d/%Y - %H:%M:%S")
    filename = now.strftime("entries/%Y/%m/%d/%H:%M:%S.txt")

    token = get_token()
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(get_remote_name())
    # If encryption key is in config, encrypt the upload
    if get_encryption_key() is not None:
        contents = encrypt_text(contents)
    repo.create_file(filename, message, contents, branch="main")


def make_readme_md():
    print("Creating readme...")
    last_date = "0000/00/00"
    output_lines = []

    token = get_token()
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(get_remote_name())
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            this_date = (file_content.path)[8:-13]
            # The 2 lines below remove files that are in the root directory, which are not logs
            if (file_content.path)[7] != '/':
                continue
            if this_date > last_date:
                output_lines.append(add_headers(last_date, this_date))
            last_date = this_date
            output_lines.append(file_content.decoded_content.decode())
    output = '\n'.join(output_lines)
    readme_contents = repo.get_contents("README.md", ref="main")
    repo.update_file("README.md", "Update README.md", output, readme_contents.sha, branch="main")


def add_headers(last_date, this_date):
    output_lines = []
    last_year = int(last_date[:4])
    last_month = int(last_date[5:-3])
    last_day = int(last_date[-2:])
    current_year = int(this_date[:4])
    current_month = int(this_date[5:-3])
    current_day = int(this_date[-2:])
    if current_year > last_year:
        output_lines.append("# " + str(current_year))
        output_lines.append("## " + str(current_month))
        output_lines.append("### " + str(current_day))
    elif current_month > last_month:
        output_lines.append("## " + str(current_month))
        output_lines.append("### " + str(current_day))
    elif current_day > last_day:
        output_lines.append("### " + str(current_day))
    output = '\n'.join(output_lines)
    return output


def encrypt_text(input):
    encoded = input.encode()
    f = Fernet(get_encryption_key())
    encrypted = f.encrypt(encoded)
    return encrypted


def decrypt_text(input):
    encoded = input.encode()
    f = Fernet(get_encryption_key())
    decrypted = f.decrypt(encoded)
    output = decrypted.decode()
    return output
