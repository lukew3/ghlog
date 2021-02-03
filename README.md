# ghlog
<!--<img src="https://github.com/lukew3/ghlog/blob/main/ghlog_logo.png?raw=true" height="100" width="100" >-->

## About
ghlog (Github Log) allows you to create a digital logbook/journal stored as a Github repository. Easily write time and date marked journal entries through the cli. [Here's an example of what a full repo might look like.](https://github.com/lukew3/ghlog-demo)

## Installation
`pip install ghlog`

After installation, you need to add a Github Personal Access Token in order for ghlog to work. To do this, [generate a personal access token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) and add it to ghlog with `ghlog config -t <personal-access-token>`

## Features

### Simplicity
All you have to do to add a log entry is run the command `ghlog` and then type your entry after the prompt.

### Security
To protect your privacy, ghlog automatically saves to a private repository so that other Github users cannot access your logs. If you are more concerned that somebody might hack your account or access your data from inside of Github, you can encrypt your logs, using `ghlog config -e`.

## Usage
* `ghlog` - Prompts the user for a new entry. Note that the personal access token must be added before this can be run.
### config
* `ghlog config -t <personal-access-token>` - Sets the personal access token to the token provided.
  * Instructions for creating a token can be found [here](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)
* `ghlog config -r <new-repo-name>` - Creates a new ghlogbook repository with the passed name. Sets as repo to write logs to.
* `ghlog config -e` - Encrypts your logs from now on. Encryption key is stored locally in .config/ghlog/config.ini file.
  * Repository is automatically set to private but encrypting logs can ease fears of account break-ins or internal snooping
  * Entries will not be readable via Github web interface.
  * Running this after an encryption key has already been set will ask if you want to overwrite old key with new key.
* `ghlog config -d` - Removes encryption. Currently encrypted logs will be decrypted and key will be removed from local storage. Logs will no longer be encrypted when added.
* `ghlog fetch <date>` - Fetches log entries from the specified date, month, or year. Date must be written in yyyy/mm/dd format
  * Can also pass a month in the format yyyy/mm or year in the format yyyy
  * If no date is specified, all logs will be fetched
  * Using the `-t` tag with no date will return logs from today
### make-readme
* `ghlog make-readme` - Makes a readme file out of submitted logs. Aiming to make this automatic possibly with github actions in a later update
* `ghlog make-readme -l` - Makes a readme file out of submitted logs and saves locally instead of on Github. If logs were encrypted, they will be stored as an unencrypted README in your current directory.
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
