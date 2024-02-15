import sys
from datetime import datetime

import questionary

from automerge import GitHubRequests, Automerge

def cli():
    try:
        run, github_key, *_ = sys.argv
    except ValueError:
        github_key = questionary.password("Write Github token with repo rights").unsafe_ask()

    requester = GitHubRequests(github_key, None, None)

    owner = questionary.select("Github owner is:", choices=requester.get_list_organizations()).unsafe_ask()
    repo = questionary.select("Github repo:", choices=requester.get_list_repositories(owner)).unsafe_ask()

    requester.owner = owner
    requester.repo = repo

    develop = questionary.text("Develop branch:", default="develop").unsafe_ask()
    res = questionary.text("Resulted branch:", default=f"test/{datetime.today().strftime('%Y%m%d%H%M')}").unsafe_ask()

    labels = requester.get_list_labels()
    label_touching = questionary.select("Need touching branches by PR label:", choices=labels).unsafe_ask()
    label_touched = questionary.select("After touched branches set label on PR:", choices=labels).unsafe_ask()

    confirmed = questionary.confirm("Are you sure?").ask()

    if not confirmed:
        exit(0)

    automerge = Automerge(
        owner=owner,
        repo=repo,
        base_branch=develop,
        mixed_branch=res,
        need_touching=label_touching,
        touched=label_touched,
        github_token=github_key,
    )
    automerge.merging(automerge.get_pulls_need_touching())
