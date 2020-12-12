# ghlog

## About
ghlog (Github Log) allows you to create a logbook and store it as a Github repository. Easily write time and date marked journal entries through the command line.

## Installation
`pip install ghlog`

## Usage
* `ghlog` - Prompts the user for a new entry. Note that the personal access token must be added before this can be run.
* `ghlog -t <personal-access-token>` - Sets the personal access token to the token provided.
  * Instructions for creating a token can be found [here](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)
* `ghlog -d <date>` - Gets log entries from the specified date. Date must be written in mm/dd/yyyy format
* `ghlog --help` - Shows the following help text:
```
Usage: ghlog [OPTIONS]

  A minimal command-line journal that saves to a Github repo

Options:
  -t, --set-token TEXT  Set Github personal access token.
  -d, --get-day TEXT    Get log entries from a certain date. Use (mm/dd/yyyy).
  --help                Show this message and exit.
```
