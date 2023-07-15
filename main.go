package main

import (
	"flag"
	"fmt"

	"github.com/jooola/find-closed-references/refs"
)

var (
	path string
)

func main() {
	// wordPtr := flag.String("word", "foo", "a string")
	// numbPtr := flag.Int("numb", 42, "an int")

	flag.StringVar(&path, "path", ".", "a string var")
	flag.Parse()
	fmt.Println(path)
	result := refs.Search(path)
	for _, ref := range result {
		fmt.Println(ref)

	}

}
