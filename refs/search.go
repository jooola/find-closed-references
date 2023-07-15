package refs

import (
	"bufio"
	"fmt"
	"io"
	"io/fs"
	"os"
	"path/filepath"
	"regexp"
	"strconv"
)

type RefScanner interface {
	GetMatchHost([][]byte) string
	GetMatchOwner([][]byte) string
	GetMatchRepo([][]byte) string
	GetMatchType([][]byte) string
	GetMatchId([][]byte) int
	GetMatchIgnore([][]byte) bool
}

type GithubRefScanner struct {
	Re            *regexp.Regexp
	reIgnoreIndex int
	reHostIndex   int
	reOwnerIndex  int
	reRepoIndex   int
	reTypeIndex   int
	reIdIndex     int
}

func NewGithubRefScanner() *GithubRefScanner {
	re := regexp.MustCompile(`(?i)` +
		`(?P<ignore>!!)?` +
		`(?:https?:\/\/)?` +
		`(?P<host>github\.com)` +
		`\/(?P<owner>[a-zA-Z\d-]+)` +
		`\/(?P<repo>[a-zA-Z\d._-]+)` +
		`\/(?P<ref_type>pull|issues)` +
		`\/(?P<ref_id>\d+)`)

	return &GithubRefScanner{
		Re:            re,
		reIgnoreIndex: re.SubexpIndex("ignore"),
		reHostIndex:   re.SubexpIndex("host"),
		reOwnerIndex:  re.SubexpIndex("owner"),
		reRepoIndex:   re.SubexpIndex("repo"),
		reTypeIndex:   re.SubexpIndex("ref_type"),
		reIdIndex:     re.SubexpIndex("ref_id"),
	}
}
func (o *GithubRefScanner) GetMatchHost(match [][]byte) string {
	return string(match[o.reHostIndex])
}
func (o *GithubRefScanner) GetMatchOwner(match [][]byte) string {
	return string(match[o.reOwnerIndex])
}
func (o *GithubRefScanner) GetMatchRepo(match [][]byte) string {
	return string(match[o.reRepoIndex])
}
func (re *GithubRefScanner) GetMatchType(match [][]byte) string {
	return string(match[re.reTypeIndex])
}
func (re *GithubRefScanner) GetMatchId(match [][]byte) int {
	value, err := strconv.Atoi(string(match[re.reIdIndex]))
	if err != nil {
		panic(err)
	}
	return value
}
func (re *GithubRefScanner) GetMatchIgnore(match [][]byte) bool {
	return len(match[re.reIgnoreIndex]) == 0
}

var githubRefScanner = NewGithubRefScanner()

func Search(root string) []*Ref {
	refs := []*Ref{}

	filepath.WalkDir(root, func(path string, d fs.DirEntry, err error) error {
		if d.IsDir() {
			return nil
		}

		fd, err := os.Open(path)
		if err != nil {
			fmt.Printf("could not open %s: %s\n", path, err)
			return nil
		}

		refs = append(refs, Scan(fd, path)...)
		return nil
	})

	return refs
}

func Scan(input io.Reader, path string) []*Ref {
	refs := []*Ref{}

	scanner := bufio.NewScanner(input)
	line := 0
	for scanner.Scan() {
		line += 1
		matches := githubRefScanner.Re.FindAllSubmatch(scanner.Bytes(), -1)
		if matches == nil {
			continue
		}

		for _, match := range matches {
			ref := &Ref{
				File:    path,
				Line:    line,
				Host:    githubRefScanner.GetMatchHost(match),
				Owner:   githubRefScanner.GetMatchOwner(match),
				Repo:    githubRefScanner.GetMatchRepo(match),
				RefType: githubRefScanner.GetMatchType(match),
				RefId:   githubRefScanner.GetMatchId(match),
				Ignore:  githubRefScanner.GetMatchIgnore(match),
			}
			refs = append(refs, ref)
		}
	}
	if err := scanner.Err(); err != nil {
		fmt.Fprintln(os.Stderr, "reading standard input:", err)
	}

	return refs
}

type Ref struct {
	File string
	Line int

	Host    string
	Owner   string
	Repo    string
	RefType string
	RefId   int
	Ignore  bool

	Closed *bool
}
