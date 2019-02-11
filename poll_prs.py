import json
from datetime import datetime, timedelta

import github_api
from notifier import Notifier

TIME_UNITS = ['days', 'seconds', 'microseconds', 'milliseconds', 'minutes', 'hours', 'weeks']

now = datetime.now()

with open('watchlist.json', 'r') as fp:
    watchlist = json.load(fp)

for repo in watchlist:
    notifier = Notifier(repo['mail'])
    delta = timedelta(**repo['timespan'])
    time_from = now - delta

    if 'branches' not in repo:
        repo['branches'] = ['master']

    for branch in repo['branches']:
        prs = github_api.get_prs_since(repo['repository'], branch, time_from)
        n = len(prs)

        for i in range(n):
            response = github_api.get_pr_files(repo['repository'], prs[i]['number'])

            for file in response:
                if file['filename'] in repo['files']:
                    notifier.append(notifier.notify_pr(file, prs[i]))

    notifier.send_notifications('[{}] A new pull request changes watched files.'.format(repo['repository']))
