import responses

from utils.branchlists import BRANCHED_LIST
from utils.created_branch import CREATED_BRANCH
from utils.pullists import MOCK_PULL_LIST


def test_get_labeled_pullrequests(mocking_automerge):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, "https://api.github.com/repos/m9sco/automerge/pulls", json=MOCK_PULL_LIST, status=200)

        pulls = mocking_automerge.get_pulls_need_touching()

        assert len(pulls) == 4
        assert pulls[0]["title"] == "Bugfix/301"
        assert pulls[1]["title"] == "fix(subscriber): redirect to global exception catcher"
        assert pulls[2]["title"] == "fix(parser): change sleep function"
        assert pulls[3]["title"] == "feat(open_chrome): add script which open chrome and substitutes local…"


def test_makepr(mocking_automerge):
    with responses.RequestsMock() as rsps:
        rsps.add(responses.GET, "https://api.github.com/repos/m9sco/automerge/git/refs", json=BRANCHED_LIST, status=200)
        rsps.add(
            responses.POST, "https://api.github.com/repos/m9sco/automerge/git/refs", json=CREATED_BRANCH, status=201
        )

        mocking_automerge.make_branch("")
