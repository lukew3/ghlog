# ghlog

## About
ghlog (Github Log) allows you to create a digital logbook/journal stored as a Github repository. Easily write time and date marked journal entries through the cli.

## Installation
`pip install ghlog`

After installation, you need to add a Github Personal Access Token in order for ghlog to work. To do this, [generate a personal access token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) and add it to ghlog with `ghlog config -t <personal-access-token>`

## Features

### Simplicity
Ghlog enables users to quickly add a log entry from the terminal by using the command `ghlog`. After `ghlog` is run, a prompt will appear and you simply type the text you wish to add.

### Security
Storing possibly sensitive information publicly is not a good idea. To protect your privacy, ghlog automatically saves to a private repository so that other Github users cannot access your logs. If you are more concerned that somebody might hack your account or access your data from inside of Github, you can encrypt your logs, using `ghlog config -e`.

## Usage
* `ghlog` - Prompts the user for a new entry. Note that the personal access token must be added before this can be run.
### config
* `ghlog config -t <personal-access-token>` - Sets the personal access token to the token provided.
  * Instructions for creating a token can be found [here](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)
* `ghlog config -r <new-repo-name>` - Creates a new ghlogbook repository with the passed name. Sets as repo to write logs to.
* `ghlog config -e` - Encrypts your logs from now on. Encryption key stored locally in .config/ghlog/config.ini file.
  * Repository is automatically set to private but encrypting logs can ease fears of account break-ins or internal snooping
  * Entries will not be readable via Github web interface.
  * Running this after an encryption key has already been set will ask if you want to overwrite old key with new key.
### fetch
* `ghlog fetch <date>` - Fetches log entries from the specified date, month, or year. Date must be written in yyyy/mm/dd format
  * Can also pass a month in the format yyyy/mm or year in the format yyyy
### make-readme
* `ghlog make-readme` - Makes a readme file out of submitted logs. Aiming to make this automatic possibly with github actions in a later update
* `ghlog make-readme -l` - Makes a readme file out of submitted logs and saves locally instead of on Github. If logs were encrypted. They will be stored as an unencrypted README in your current directory.
### --help page
* `ghlog --help` - Shows the following help text:
```
Usage: ghlog [OPTIONS] COMMAND [ARGS]...

  A minimal command-line journal that saves to a Github repo

Options:
  --help  Show this message and exit.

Commands:
  config       Configure ghlog.
  fetch        Returns logs from the passed date (Use format yyyy/mm/dd)
  make-readme  Makes readme in Github repo out of uploaded logs
```
