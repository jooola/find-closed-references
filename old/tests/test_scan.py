import pytest

from find_closed_references.search import (
    GITHUB_REFS_RE,
    GITLAB_REFS_RE,
    scan_dir,
    scan_file,
)

from .fixtures import fixtures_file_refs, fixtures_path


@pytest.mark.parametrize(
    "url, expected_refs",
    [
        ("github.com/user/repo/issues/1", {"ref_type": "issues", "ref_id": "1"}),
        ("github.com/user/repo/pull/10", {"ref_type": "pull", "ref_id": "10"}),
    ],
)
@pytest.mark.parametrize("ignore", ["", "!!"])
@pytest.mark.parametrize("scheme", ["", "http://", "https://"])
def test_github_refs_re(url, expected_refs, ignore, scheme):
    candidate = f"{ignore}{scheme}{url}"
    matches = GITHUB_REFS_RE.search(candidate)

    common = {"host": "github.com", "owner": "user", "repo": "repo"}
    assert matches is not None
    assert matches.groupdict() == {"ignore": ignore or None, **common, **expected_refs}


@pytest.mark.parametrize(
    "url, expected_refs",
    [
        ("gitlab.com/user/repo/-/issues/1", {"ref_type": "issues", "ref_id": "1"}),
        (
            "gitlab.com/user/repo/-/merge_requests/10",
            {"ref_type": "merge_requests", "ref_id": "10"},
        ),
    ],
)
@pytest.mark.parametrize("ignore", ["", "!!"])
@pytest.mark.parametrize("scheme", ["", "http://", "https://"])
def test_gitlab_refs_re(url, expected_refs, ignore, scheme):
    haystack = f"{ignore}{scheme}{url}"
    matches = GITLAB_REFS_RE.search(haystack)

    common = {"host": "gitlab.com", "owner": "user", "repo": "repo"}

    assert matches is not None
    assert matches.groupdict() == {"ignore": ignore or None, **common, **expected_refs}


def test_scan_file():
    result = scan_file(fixtures_path / "file.md")
    assert result == fixtures_file_refs


def test_scan_dir():
    result = scan_dir(fixtures_path)
    assert result == fixtures_file_refs
