import logging
import typing

import requests

from automerge.GitHubRequests import GitHubRequests


class Automerge:
    def __init__(
        self,
        owner,
        repo,
        base_branch,
        mixed_branch,
        need_touching,
        touched,
        github_token,
    ):
        self.owner: str = owner
        self.repo: str = repo
        self.base_branch: str = base_branch
        self.mixed_branch: str = mixed_branch
        self.need_touching: str = need_touching
        self.touched: str = touched
        self.github_token: str = github_token

        self._github_requests = GitHubRequests(github_token, self.owner, self.repo)

    def get_pulls_need_touching(self) -> typing.List[typing.Dict]:
        pulls = self._github_requests.get_opened_pulls()
        return [p for p in pulls if list(filter(lambda label: label["name"] == self.need_touching, p["labels"]))]

    def merging(self, pulls):
        if not pulls:
            return

        self._github_requests.create_branch(name=self.mixed_branch, base=self.base_branch)

        for pull in pulls:
            labels = [i["name"] for i in pull["labels"] if i["name"] != self.need_touching] + [self.touched]
            pr = self._github_requests.create_pull(base=self.mixed_branch, head=pull["head"]["ref"])
            transit_pr_num = pr["url"].rsplit("/", 1)[-1]
            pull_num = pull["url"].rsplit("/", 1)[-1]
            self._github_requests.set_labels(pull_number=pull_num, new_label_list=labels)
            try:
                self._github_requests.merge_pull(pull_number=transit_pr_num)
            except requests.exceptions.RequestException:
                logging.error(f"Something got wrong with merge from {transit_pr_num} to {pull_num}")

            # self._github_requests.merging_branch(base=self.base_branch, head=pull["head"]["ref"])

        result_pr = self._github_requests.create_pull(base=self.base_branch, head=self.mixed_branch)
        result_pr_num = result_pr["url"].rsplit("/", 1)[-1]
        for pull in pulls:
            self._github_requests.commenting(pull["url"].rsplit("/", 1)[-1], message=f"#{result_pr_num}")
