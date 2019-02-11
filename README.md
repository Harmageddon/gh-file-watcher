# gh-file-watcher
Monitors files on GitHub repositories and notifies you about changes. It uses the public GitHub API and can be run as a cron job for automatic monitoring.

## Requirements

- Python 3.x with Pip
- Requests package for Python (installable via pip, see (#Installation)[Installation]

## Installation

If you are working on your own system, you can use Python and Pip right away:

```
pip install -r requirements.txt
```

...and you are done.

If the scripts should be run on a shared machine (e.g. on hosted webspace), you need SSH access. 
You can install a local version of Python and use it like this:

```
pyenv venv
venv/bin/pip install -r requirements.txt
```

When using this tool, you need to replace `python` by `venv/bin/python` (prefixed with the path to the directory of gh-file-watcher).

## Usage
In order to programmatically monitor all changes, it is recommended to set up a cron job running the commands and to set the time span in the watchlist to the frequency the cron job is run. 
This way, you won't miss any changes to files you want to know about!

### Create a Watchlist

Create a file `watchlist.json` in the project's directory. It has the following structure:

```json
[
  {
    "repository": "username/repo1",
    "branches": ["master", "staging"],
    "files": [
      "path/to/important/file1.py",
      "path/to/important/file2.ini"
    ],
    "mail": "user@example.org, colleague@example.org",
    "timespan": {
      "days": 1
    }
  },
  {
    "repository": "user2/repo2",
    "branches": ["master"],
    "files": [
      "path/to/important/file1.py"
    ],
    "mail": "user@example.org",
    "timespan": {
      "days": 1
    }
  }
]
```

- `repository` defines the path to the repository on GitHub, containing the owner and the repository's name.
- `branches` is an array of all branches you want to monitor for changes.
- `files` is an array of all files you want to watch.
- `mail` is your mail address. If you want to send the notifications to multiple mail addresses, enter them comma-separated.
- `timespan` is an object defining the timespan you want to monitor. For example, when using one day here, `poll_prs.py` will check for pull requests updated within the last 24 hours.
  For possible attributes, see https://docs.python.org/3/library/datetime.html#timedelta-objects.

### Monitor Pull Requests

By running 

```
python poll_prs.py
```

the application retrieves all pull requests changed within the given timespan that change one of the files defined in the watchlist.
It then sends notifications about the changes to the defined mail addresses.
