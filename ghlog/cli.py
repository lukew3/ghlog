import click
import os
import configparser
from github import Github
from datetime import datetime
from .config_access import set_token, get_token, get_remote_name
import time
from multiprocessing.pool import ThreadPool


@click.command()
@click.option('-t', '--set-token', 'token', help='Set Github personal access token.')
# @click.option('-r', '--set-repo', 'repo_name', help='Set name of Github repository where logbook is stored')
@click.option('-d', '--get-day', 'date', help='Get log entries from a certain date. Use (mm/dd/yyyy).')
@click.option('-m', '--make-readme', help='Combines all logs into the Github README', is_flag=True)
def cli(token, date, make_readme):
    """ A minimal command-line journal that saves to a Github repo """
    if token is not None:
        set_token(token)
        return None

    if date is not None:
        print(get_logs_by_date(date))
        return None

    if make_readme:
        make_readme_md()
        return None

    config_file = os.path.expanduser("~") + "/.config/ghlog/config.ini"
    # This doesn't work if token was deleted from file, which is unlikely but still possible
    if not os.path.exists(config_file):
        print("No personal access token added. To set token, user 'ghlog -s <token>'")
        print("Get help setting up at https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token. Only repo permission is necessary.")
        return None

    add_entry()


def get_logs_by_date(datestring):
    output_lines = []
    token = get_token()
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(get_remote_name())
    contents = repo.get_contents("README.md", ref="main")
    lines = contents.decoded_content.decode()
    month_number = int(datestring[:2])
    datetime_object = datetime.strptime(str(month_number), "%m")
    month_name = datetime_object.strftime("%B")
    day = int(datestring[3:-5])
    year = int(datestring[-4:])
    yearCorrect = False
    monthCorrect = False
    dayCorrect = False
    linesList = lines.splitlines()
    """
    What this loop does:
    * Goes down the list until it finds the desired year
    * sets yearcorrect to true as long as a new year isn't encountered
    * does the same for month and day
    * If day is found, all lines below it are returned until dayCorrect is set to False
      * This is done when a new year, month, or date is encountered
    """
    for line in linesList:
        if line[:2] == "# ":
            if line[2:] == str(year):
                yearCorrect = True
            else:
                yearCorrect = False
                dayCorrect = False
        elif line[:3] == "## ":
            if line[3:] == str(month_name) and yearCorrect:
                monthCorrect = True
            else:
                monthCorrect = False
                dayCorrect = False
        elif line[:4] == "### ":
            if line[4:] == str(day) and yearCorrect and monthCorrect:
                dayCorrect = True
                # Continue statement prevents the line with the date in it from being returned
                continue
            else:
                dayCorrect = False

        if dayCorrect:
            output_lines.append(line)

    output = '\n'.join(output_lines)
    if output == '':
        output = "No entries for that date"
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
    current_time = now.strftime("%H:%M:%S")
    contents = entry + '\n'
    message = now.strftime("%m/%d/%Y - %H:%M:%S")
    filename = now.strftime("entries/%Y/%m/%d/%H:%M:%S.txt")

    token = get_token()
    g = Github(token)
    user = g.get_user()
    repo = user.get_repo(get_remote_name())
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
    elif current_date > last_day:
        output_lines.append("### " + str(current_day))
    output = '\n'.join(output_lines)
    return output
