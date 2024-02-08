import hashlib
import json
import logging
import traceback

import requests


class GitHubRequests:

    def __init__(self, token, owner, repo):
        self.token = token
        self.owner = owner
        self.repo = repo

    def _request(self, url, headers_addons=None, json=None, method: str = "GET"):
        if not headers_addons:
            headers_addons = {}
        headers = {**self._get_default_headers(), **headers_addons}

        try:
            res = requests.request(method=method, url=url, headers=headers, json=json)
            logging.info(res.text)
            return res
        except:
            logging.error(traceback.format_exc())

    def _get_default_headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Accept": "application/vnd.github+json",
        }

    def make_url_on_repo(self, depart, endswith):
        return f"https://api.github.com/{depart}/{self.owner}/{self.repo}/{endswith}"

    @staticmethod
    def make_url(depart):
        return f"https://api.github.com/{depart}"

    def get_opened_pulls(self):
        url = self.make_url_on_repo("repos", "pulls")

        response = self._request(
            url,
        )  # state="open" is default
        assert response.status_code == 200

        return json.loads(response.text)

    def create_pull(self, base, head):
        url = self.make_url_on_repo("repos", "pulls")
        response = self._request(url, json={"head": head, "base": base, "title": head}, method="POST")
        assert response.status_code == 201
        return json.loads(response.text)

    def create_branch(self, name: str, base: str):
        url = self.make_url_on_repo("repos", "git/refs")

        branches = self._request(url)
        assert branches.status_code == 200
        branches_json = json.loads(branches.text)
        branch = next(filter(lambda branch: branch["ref"] == "refs/heads/" + base, branches_json), None)
        assert branch is not None
        response = self._request(url, json={"ref": f"refs/heads/{name}", "sha": branch["object"]["sha"]}, method="POST")
        assert response.status_code == 201
        return json.loads(response.text)

    def merge_pull(self, pull_number):
        url = self.make_url_on_repo("repos", f"pulls/{pull_number}/merge")
        merge_pr = self._request(url, method="PUT")
        assert merge_pr.status_code == 200

    def merging_branch(self, base, head):
        url = self.make_url_on_repo("repos", "merges")
        request = self._request(url, json={"base": base, "head": head}, method="POST")
        assert request.status_code in [201, 204]

    def set_labels(self, pull_number, new_label_list):
        url = self.make_url_on_repo("repos", f"issues/{pull_number}/labels")
        set_labels = self._request(url, method="PUT", json={"labels": new_label_list})
        assert set_labels.status_code == 200

    def commenting(self, pull_number, message):
        url = self.make_url_on_repo("repos", f"issues/{pull_number}/comments")
        set_labels = self._request(url, method="POST", json={"body": message})
        assert set_labels.status_code == 201

    def get_list_organizations(self):

        user = self._request(self.make_url("user"), method="GET")
        organizations = self._request(self.make_url("user/orgs"), method="GET")
        assert organizations.status_code == 200
        assert user.status_code == 200
        organizations = [org["login"] for org in json.loads(organizations.text)]

        return [json.loads(user.text)["login"]] + organizations

    def get_list_repositories(self, org: str):
        repos = self._request(self.make_url(f"orgs/{org}/repos"), method="GET")
        assert repos.status_code == 200
        return json.loads(repos.text)

    def get_list_labels(self):
        labels = self._request(self.make_url_on_repo("repos", "labels"), method="GET")

        assert labels.status_code == 200
        return json.loads(labels.text)
