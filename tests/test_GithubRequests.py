import responses

from utils.branchlists import BRANCHED_LIST
from utils.created_branch import CREATED_BRANCH
from utils.created_pull import CREATED_PULL
from utils.pullists import MOCK_PULL_LIST


def test_make_sure_url(mocking_GitHubRequests):
    url = mocking_GitHubRequests.make_url_on_repo("repos", "pulls")

    assert url == "https://api.github.com/repos/m9sco/automerge/pulls"


def test_make_sure_headers(mocking_GitHubRequests):
    headers = mocking_GitHubRequests._get_default_headers()
    assert headers == {
        "Authorization": "Bearer tested",
        "X-GitHub-Api-Version": "2022-11-28",
        "Accept": "application/vnd.github+json",
    }


def test_get_opened_pullrequests(mocking_GitHubRequests):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, "https://api.github.com/repos/m9sco/automerge/pulls", json=MOCK_PULL_LIST, status=200)
        result = mocking_GitHubRequests.get_opened_pulls()
        assert result == MOCK_PULL_LIST


def test_make_pull(mocking_GitHubRequests):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.POST, "https://api.github.com/repos/m9sco/automerge/pulls", json=CREATED_PULL, status=201)
        result = mocking_GitHubRequests.create_pull(base="develop", head="test")
        assert result == CREATED_PULL


def test_make_ref(mocking_GitHubRequests):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, "https://api.github.com/repos/m9sco/automerge/git/refs", json=BRANCHED_LIST, status=200)
        rsps.add(
            responses.POST, "https://api.github.com/repos/m9sco/automerge/git/refs", json=CREATED_BRANCH, status=201
        )
        result = mocking_GitHubRequests.create_branch(base="develop", name="test")
        assert result == CREATED_BRANCH
