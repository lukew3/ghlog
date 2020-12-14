# ghlog

## About
ghlog (Github Log) allows you to create a digital logbook/journal stored as a Github repository. Easily write time and date marked journal entries through the command line.

## Installation
`pip install ghlog`

## Usage
* `ghlog` - Prompts the user for a new entry. Note that the personal access token must be added before this can be run.
* `ghlog -t <personal-access-token>` - Sets the personal access token to the token provided.
  * Instructions for creating a token can be found [here](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)
* `ghlog -r <new-repo-name>` - Creates a new ghlogbook repository with the passed name
* `ghlog -d <date>` - Gets log entries from the specified date. Date must be written in yyyy/mm/dd format
  * Can also pass a month in the format yyyy/mm or year in the format yyyy
* `ghlog -m` - Makes a readme file out of submitted logs. Aiming to make this automatic possibly with github actions in a later update
* `ghlog -e` - Encrypts your logs from now on. Encryption key stored locally in .config/ghlog/config.ini file.
  * Repository is automatically set to private but encrypting logs can ease fears of account break-ins or internal snooping
  * Entries will not be readable via Github web interface.
* `ghlog --help` - Shows the following help text:
```
Usage: ghlog [OPTIONS]

  A minimal command-line journal that saves to a Github repo

Options:
  -t, --set-token TEXT    Set Github personal access token.
  -r, --create-repo TEXT  Create new Github repo with passed name.
  -d, --get-day TEXT      Get log entries from a certain date, month, or year.
                          Use (yyyy/mm/dd) and stop after your desired time.
                          Ex: 2020/12 for December 2020, 2019/08/15 for August
                          15th 2019

  -m, --make-readme       Combines all logs into the Github README
  -e, --encrypt           Encrypt your logs from now on. Warning: your logs
                          will not be readable on Github, they must be
                          decrypted locally to be readable.

  --help                  Show this message and exit.
```
