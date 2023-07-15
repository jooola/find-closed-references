import logging
import os
import re
from itertools import chain
from typing import List

from pathspec import GitIgnoreSpec

from ._ref import Ref

logger = logging.getLogger(__name__)


GITHUB_REFS_RE = re.compile(
    r"(?P<ignore>!!)?"
    r"(?:https?:\/\/)?"
    r"(?P<host>github\.com)"
    r"\/(?P<owner>[a-zA-Z\d-]+)"
    r"\/(?P<repo>[a-zA-Z\d._-]+)"
    r"\/(?P<ref_type>pull|issues)"
    r"\/(?P<ref_id>\d+)",
    re.IGNORECASE,
)

GITLAB_REFS_RE = re.compile(
    r"(?P<ignore>!!)?"
    r"(?:https?:\/\/)?"
    r"(?P<host>gitlab\.com)"
    r"\/(?P<owner>[a-zA-Z\d-]+)"
    r"\/(?P<repo>[a-zA-Z\d._-]+)"
    r"\/-"
    r"\/(?P<ref_type>merge_requests|issues)"
    r"\/(?P<ref_id>\d+)",
    re.IGNORECASE,
)


def scan_file(
    path: str,
    ignored_refs: List[str] = [],
) -> list[Ref]:
    logger.debug(f"scanning file {path}")
    try:
        with open(path, encoding="utf8") as file:
            content = file.read()
    except UnicodeError:
        return []

    refs: list[Ref] = []
    for re_match in chain(
        GITHUB_REFS_RE.finditer(content),
        GITLAB_REFS_RE.finditer(content),
    ):
        line = content.count("\n", 0, re_match.start()) + 1
        refs.append(
            Ref(
                file=path,
                line=line,
                **re_match.groupdict(),
            )
        )

    return refs


def scan_dir(
    path: str,
    ignored_files: GitIgnoreSpec = None,
    ignored_refs: List[str] = [],
) -> list[Ref]:
    logger.debug(f"scanning dir {path}")

    refs = []
    for root, _, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if ignored_files and ignored_files.match_file(file_path):
                continue

            file_refs = scan_file(file_path, ignored_refs)
            refs.extend(file_refs)

    return refs
