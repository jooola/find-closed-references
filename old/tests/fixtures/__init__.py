from pathlib import Path

from find_closed_references._ref import Ref

fixtures_path = Path(__file__).parent.relative_to(Path.cwd())

fixtures_file = fixtures_path / "file.md"
fixtures_file_refs = [
    Ref(
        file=str(fixtures_file),
        line=3,
        host="github.com",
        owner="user",
        repo="repo",
        ref_type="issues",
        ref_id=10,
        ignore=False,
    ),
    Ref(
        file=str(fixtures_file),
        line=4,
        host="github.com",
        owner="user",
        repo="repo",
        ref_type="pull",
        ref_id=10,
        ignore=False,
    ),
    Ref(
        file=str(fixtures_file),
        line=5,
        host="github.com",
        owner="user",
        repo="repo",
        ref_type="pull",
        ref_id=10,
        ignore=True,
    ),
    Ref(
        file=str(fixtures_file),
        line=7,
        host="gitlab.com",
        owner="user",
        repo="repo",
        ref_type="issues",
        ref_id=10,
        ignore=False,
    ),
    Ref(
        file=str(fixtures_file),
        line=8,
        host="gitlab.com",
        owner="user",
        repo="repo",
        ref_type="merge_requests",
        ref_id=10,
        ignore=False,
    ),
    Ref(
        file=str(fixtures_file),
        line=9,
        host="gitlab.com",
        owner="user",
        repo="repo",
        ref_type="merge_requests",
        ref_id=10,
        ignore=True,
    ),
]
