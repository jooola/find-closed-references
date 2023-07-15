from requests import Session
from ._ref import Ref
import os
import logging
from functools import cache

logger = logging.getLogger(__name__)


class GithubClient:
    def __init__(self) -> None:
        self._session = Session()
        self._session.headers.update({"Accept": "application/vnd.github+json"})

        if "GITHUB_TOKEN" in os.environ:
            github_token = os.environ.get("GITHUB_TOKEN")
            self._session.headers.update({"Authorization": f"Token {github_token}"})

    def is_ref_closed(self, ref: Ref) -> bool:
        url = f"https://api.github.com/repos/{ref.owner}/{ref.repo}/issues/{ref.ref_id}"
        with self._session.get(url) as resp:
            resp.raise_for_status()
            payload = resp.json()
            return payload.get("state") == "closed"


@cache
def get_github_client() -> GithubClient:
    return GithubClient()
