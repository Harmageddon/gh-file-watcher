import json

import github_api
from notifier import Notifier

with open('watchlist.json', 'r') as fp:
    watchlist = json.load(fp)

try:
    with open('hashes.json', 'r') as fp:
        hashes = json.load(fp)
except FileNotFoundError:
    hashes = {}


def file_path(repo, file):
    return '{}/{}'.format(repo, file)


def url_commit(repo, sha):
    return 'https://github.com/{}/commit/{}'.format(repo, sha)


for repo in watchlist:
    notifier = Notifier(repo['mail'])

    try:
        if 'branches' not in repo:
            repo['branches'] = ['master']

        if repo['repository'] not in hashes:
            hashes[repo['repository']] = {}

        for branch in repo['branches']:
            if branch not in hashes[repo['repository']]:
                hashes[repo['repository']][branch] = {}

            for file in repo['files']:
                response = github_api.get_file(repo['repository'], file)
                sha = response['sha']

                path = file_path(repo['repository'], file)

                if file in hashes[repo['repository']][branch] and hashes[repo['repository']][branch][file] != sha:
                    response = github_api.get_file_commits(repo['repository'], file)
                    commit = response[0]

                    notifier.append(notifier.notify_commit(file, commit))
                    hashes[repo['repository']][branch][file] = sha

        notifier.send_notifications('[{}] A new commit changed watched files.'.format(repo['repository']))

    except PermissionError as e:
        notifier.append(notifier.error(e.args[0]), '[{}] API Error!'.format(repo['repository']))
        notifier.send_notifications('[{}] A new commit changed watched files.'.format(repo['repository']))
        raise e

with open('hashes.json', 'w') as fp:
    json.dump(hashes, fp)
