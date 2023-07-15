from pathspec import GitIgnoreSpec
from typing import List

from ._ref import Ref


def get_ignored_refs(ignores_path: str) -> List[Ref]:
    with open(ignores_path, encoding="utf-8") as ignores_fd:
        lines = ignores_fd.readlines()

    lines = [line for line in lines if not line.startswith("#")]

    return lines


def get_ignored_files(ignores_path: str) -> GitIgnoreSpec:
    with open(ignores_path, encoding="utf-8") as ignores_fd:
        lines = ignores_fd.readlines()

    lines.append(".git")
    return GitIgnoreSpec.from_lines(lines)
