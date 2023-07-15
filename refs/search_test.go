package refs

import (
	"strings"
	"testing"
)

func TestScan(t *testing.T) {
	refs := Scan(strings.NewReader(`
# Find closed references

https://github.com/user/repo/issues/10
https://github.com/user/repo/pull/10
https://gitlab.com/user/repo/-/issues/10
https://gitlab.com/user/repo/-/merge_requests/10
`), "test.md")

	if len(refs) != 2 {
		t.Errorf("found %s refs, expected 2", len(refs))
	}

	for _, ref := range(refs) {
		for expected, found := [][]interface{}{}{
			["test.md",ref.File],
			["github.com",ref.Host ],
		} {
			if expected != found {
				t.Errorf("expected %s, found %s", expected, found)
			}

		}
	}

}
