from find_closed_references._ignores import get_ignored_refs

from .fixtures import fixtures_path


def test_get_ignored_refs():
    result = get_ignored_refs(str(fixtures_path / ".refsignore"))
    assert result == []
