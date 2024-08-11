package main

import (
	"flag"
	"fmt"
	"log"
	"os"
	"runtime/pprof"
	"strings"

	"job-scraper/parsers"

	"github.com/geziyor/geziyor"
	"github.com/geziyor/geziyor/export"
)

func main() {
	// checking to see how much memory a set would use
	// later write this so that it only runs in dev mode??
	f, err := os.Create("mem.prof")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	if err := pprof.WriteHeapProfile(f); err != nil {
		log.Fatal(err)
	}

	// allowing different websites and search terms to be passed in
	var (
		// baseUrl    string
		roleSearch string
		toExport   bool
	)
	// make this a switch statement will work on it later when I add different parsers
	// flag.StringVar(&baseUrl, "url", "https://www.seek.com.au", "The base URL to scrape")
	flag.StringVar(&roleSearch, "roles", "software", "The role to search for")
	flag.Parse()
	roleSearch = strings.Replace(roleSearch, " ", "-", -1) + "-jobs"

	options := geziyor.Options{
		StartURLs: []string{fmt.Sprintf("https://www.seek.com.au/%s", roleSearch)},
		ParseFunc: parsers.SeekRolesParse,
	}

	if toExport {
		options.Exporters = append(options.Exporters, &export.JSON{})
	}

	geziyor.NewGeziyor(&options).Start()
}
