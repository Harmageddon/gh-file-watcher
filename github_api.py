import requests
from datetime import datetime

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


def get_prs(repo, branch, page=1):
    url = 'https://api.github.com/repos/{}/pulls?base={}&sort=updated&direction=desc&page={:d}'.format(repo, branch, page)

    return api_call(url)


def get_pr_files(repo, number):
    url = 'https://api.github.com/repos/{}/pulls/{:d}/files'.format(repo, number)

    return api_call(url)


def get_prs_since(repository, branch, since):
    prs = get_prs(repository, branch)
    i_filtered = 0
    page = 1

    while datetime.strptime(prs[i_filtered]['updated_at'], DATE_FORMAT) > since:
        i_filtered += 1

        if i_filtered >= len(prs):
            page += 1
            response = get_prs(repository, branch, page)

            if len(response) == 0:
                break

            prs.extend(response)

    return prs[:i_filtered]


def get_file(repo, file):
    url = 'https://api.github.com/repos/{}/contents/{}'.format(repo, file)

    return api_call(url)


def get_file_commits(repo, file):
    url = 'https://api.github.com/repos/{}/commits?path={}'.format(repo, file)

    return api_call(url)


def api_call(url):
    response = requests.get(url)

    if response.status_code == 403:
        raise PermissionError(response.json()['message'])

    return response.json()
