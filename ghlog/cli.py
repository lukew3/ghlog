import click
import os
import configparser
from github import Github
from datetime import datetime
from .config_access import set_token, get_token, get_remote_name, make_encryption_key, get_encryption_key, get_config_file, make_empty_config, remove_encryption_key
import time
from tqdm import tqdm
from multiprocessing.pool import ThreadPool
from cryptography.fernet import Fernet


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """ A minimal command-line journal that saves to a Github repo """
    # Check if config is setup before run, set up if not made yet
    if not os.path.exists(get_config_file()):
        make_empty_config()
    # If no subcommands are passed this is run
    if ctx.invoked_subcommand is None:
        if get_token() == '':
            print("No personal access token added. To set token, user 'ghlog config -t <token>'")
            print("Get help setting up at https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token. Only repo permission is necessary.")
            return None
        add_entry()


@cli.command()
@click.option('-t', '--set-token', 'new_token', help='Set Github personal access token.')
@click.option('-e', '--encrypt', help='Encrypt your logs from now on. Warning: your logs will not be readable on Github, they must be decrypted locally to be readable.', is_flag=True)
@click.option('-d', '--decrypt', help='Removes encryption. Currently encrypted logs will be decrypted and key will be removed from local storage. Logs will no longer be encrypted when added', is_flag=True)
@click.option('-r', '--repo', 'new_repo_name', help='Name the repository you want logs to be stored in. If it does not exist, it will be created for you.')
def config(encrypt, decrypt, new_token, new_repo_name):
    """ Configure ghlog. See ghlog config --help for options """
    if encrypt:
        activate_encryption()

    if decrypt:
        remove_encryption()

    if new_token is not None:
        set_token(new_token)

    if new_repo_name is not None:
        # Check if repo exists before creating it
        create_repo(repo_name=new_repo_name)


@cli.command()
@click.argument('datestring', default='')
@click.option('-t', '--today', is_flag=True)
def fetch(datestring, today):
    """ Returns logs from the passed date (Use format yyyy/mm/dd)"""
    output_lines = []
    output = ""
    token = get_token()
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(get_remote_name())
    if today and datestring == '':
        now = datetime.now()
        datestring = now.strftime("%Y/%m/%d")
    try:
        contents = repo.get_contents("entries/" + datestring)
        # Count number of files; This takes about half a second for 20 files
        file_count = 0
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                file_count += 1

        # initialize progress bar
        pbar = tqdm(total=file_count)
        # Get file contents and add to output_lines
        contents = repo.get_contents("entries/" + datestring)
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                log_contents = file_content.decoded_content.decode()
                if get_encryption_key() != '':
                    log_contents = decrypt_text(log_contents)
                output_lines.append(log_contents)
                pbar.update(1)
        output = '\n'.join(output_lines)
        pbar.close()
    except Exception:
        output = "No entries found for specified day(s)"
    print(output)


@cli.command()
# Add option to store locally
@click.option('-l', '--local', 'local', help='Save the README.md file locally to cwd', is_flag=True)
def make_readme(local):
    """ Makes readme in Github repo out of uploaded logs """
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
            if local:
                output_lines.append(decrypt_text(file_content.decoded_content.decode()))
            else:
                output_lines.append(file_content.decoded_content.decode())
    output = '\n'.join(output_lines)
    readme_contents = repo.get_contents("README.md", ref="main")
    if local:
        with open("README.md", 'w') as g:
            g.write(output)
    else:
        repo.update_file("README.md", "Update README.md", output, readme_contents.sha, branch="main")


def create_repo(repo_name="mylog"):
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
    if get_remote_name() == '':
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
    if get_encryption_key() != '':
        contents = encrypt_text(contents)
    repo.create_file(filename, message, contents, branch="main")


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


def activate_encryption():
    make_encryption_key()
    encrypted_line = ""
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
            # The 2 lines below remove files that are in the root directory, which are not logs
            if (file_content.path)[7] != '/':
                continue
            encrypted_line = encrypt_text(file_content.decoded_content.decode())
            file = repo.get_contents(file_content.path, ref="main")
            repo.update_file(file_content.path, "Encrypt logs", encrypted_line, file.sha, branch="main")


def remove_encryption():
    decrypted_line = ""
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
            # The 2 lines below remove files that are in the root directory, which are not logs
            if (file_content.path)[7] != '/':
                continue
            decrypted_line = decrypt_text(file_content.decoded_content.decode())
            file = repo.get_contents(file_content.path, ref="main")
            repo.update_file(file_content.path, "Decrypt logs", decrypted_line, file.sha, branch="main")
    remove_encryption_key()
