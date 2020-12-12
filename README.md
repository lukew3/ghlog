# ghlog

## About
ghlog (Github Log) allows you to create a logbook and store it as a Github repository. You can easily add entries through the command line.

## Installation
`pip install ghlog`

## Usage
* `ghlog` - Prompts the user for a new entry. Note that the personal access token must be added before this can be run.
* `ghlog -s <personal-access-token>` - Sets the personal access token to the token provided.
  * Instructions for creating a token can be found [here](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)
* `ghlog --help` - Shows the following help text:
```
Usage: ghlog [OPTIONS]

  A minimal command-line journal that saves to a Github repo

Options:
  -s, --set-token TEXT  Set Github personal access token.
  --help                Show this message and exit.
```
