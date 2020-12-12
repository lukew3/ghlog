import click
import os
import configparser
from github import Github
from datetime import datetime
from .config_access import set_token, get_token, get_remote_name, get_last_update, set_last_update_to_now

@click.command()
@click.option('-s', '--set-token', 'token', help='Set Github personal access token.')
def cli(token):
    """ A minimal command-line journal that saves to a Github repo """
    if token != None:
        set_token(token)
        return 0

    config_file = os.path.expanduser("~") + "/.config/ghlog/config.ini"
    if not os.path.exists(config_file):
        print("No personal access token added. To set token, user 'ghlog -s <token>'")
        print("Get help setting up at https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token. Only repo permission is necessary.")
        return 0

    add_entry()


def create_repo(repo_name="My-ghlog"):
    token = get_token()
    g = Github(token)
    user = g.get_user()
    repos = user.get_repos()
    print("Creating Github repo...")
    repo = user.create_repo(repo_name, private=True)
    # Add README.md with title to github
    titlebar = '='*len(repo_name)
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
    if get_remote_name() == None:
        # Ask what the user would like to call their repo before creating it; default to My-ghlog
        create_repo()
    token = get_token()
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(get_remote_name())
    contents = repo.get_contents("README.md", ref="main")
    # Prompts user for their entry
    entry = input("Write your entry: ")
    # Quit the process if an empty entry is entered
    if entry == "":
        print("Entry discarded")
        return 0
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # add upload contents to new_contents
    new_contents = contents.decoded_content.decode()
    new_contents += add_headers()
    new_contents += '\n' + current_time + " - " + entry + '\n'
    message = now.strftime("%m/%d/%Y - %H:%M:%S")
    # Update file
    repo.update_file(contents.path, message, new_contents, contents.sha, branch="main")
    # Set last updated date
    set_last_update_to_now()


def add_headers():
    # This could probably look a little nicer
    output_lines = []
    now = datetime.now()
    last_update = get_last_update()
    last_year = int(last_update[-4:])
    last_month = int(last_update[:2])
    last_date = int(last_update[3:-5])
    current_year = int(now.strftime("%Y"))
    current_month = int(now.strftime("%m"))
    current_date = int(now.strftime("%d"))
    if current_year > last_year:
        output_lines.append("# " + str(current_year))
        output_lines.append("## " + now.strftime("%B"))
        output_lines.append("### " + str(current_date))
    elif current_month > last_month:
        output_lines.append("## " + now.strftime("%B"))
        output_lines.append("### " + str(current_date))
    elif current_date > last_date:
        output_lines.append("### " + str(current_date))
    output = '\n'.join(output_lines)
    return output
