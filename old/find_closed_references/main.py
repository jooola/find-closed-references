import logging
import os
from argparse import ArgumentParser

from pathspec import GitIgnoreSpec

from .search import scan_dir
from pprint import pprint
from ._clients import get_github_client
from ._ignores import get_ignored_files, get_ignored_refs


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("path", default=os.getcwd())
    parser.add_argument("--ignore-file", default=".gitignore")
    parser.add_argument("--ignore-refs", default=".refsignore")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    ignored_files = get_ignored_files(args.ignore_file)
    ignored_refs = get_ignored_refs(args.ignore_refs)

    refs = scan_dir(
        args.path,
        ignored_files=ignored_files,
        ignored_refs=ignored_refs,
    )

    github_client = get_github_client()
    for ref in refs:
        if ref.host == "github.com":
            ref.closed = github_client.is_ref_closed(ref)

    pprint(refs)

    return 0


if __name__ == "__main__":
    SystemExit(main())
