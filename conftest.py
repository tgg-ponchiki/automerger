import logging
import pytest

from automerge import Automerge
from automerge.GitHubRequests import GitHubRequests

logging.basicConfig(level=logging.INFO)


@pytest.fixture()
def mocking_GitHubRequests():
    requester = GitHubRequests("tested", "m9sco", "automerge")

    return requester


@pytest.fixture()
def mocking_automerge():
    automerge = Automerge(
        owner="m9sco",
        repo="automerge",
        base_branch="develop",
        mixed_branch="test/date",
        need_touching="Нужно тестирование",
        touched="На тесте",
        github_token="tested",
    )

    return automerge
