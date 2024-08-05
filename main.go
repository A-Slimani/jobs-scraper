package main

import (
	"context"
	"encoding/base64"
	"fmt"
	"log"
	"os"
	"runtime/pprof"
	"strings"

	"github.com/PuerkitoBio/goquery"
	"github.com/geziyor/geziyor"
	"github.com/geziyor/geziyor/client"
	"github.com/geziyor/geziyor/export"
	"github.com/jackc/pgx/v5"
	"github.com/jackc/pgx/v5/pgconn"
	"github.com/joho/godotenv"
)

type Job struct {
	Id       string `json:"id"`
	Title    string `json:"title"`
	Company  string `json:"company"`
	Salary   string `json:"salary"`
	Location string `json:"location"`
	Link     string `json:"link"`
	Website  string `json:"website"`
}

func main() {
	// checking to see how much memory a set would use
	f, err := os.Create("mem.prof")
	if err != nil {
		log.Fatal(err)
	}
	defer f.Close()
	if err := pprof.WriteHeapProfile(f); err != nil {
		log.Fatal(err)
	}

	options := geziyor.Options{
		StartURLs: []string{"https://www.seek.com.au/computer-science-graduate-jobs/in-All-Sydney-NSW"},
		ParseFunc: rolesParse,
		Exporters: []export.Exporter{&export.JSON{}},
	}
	geziyor.NewGeziyor(&options).Start()
}

func createDbConn() *pgx.Conn {
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Error loading .env file")
	}
	conn, err := pgx.Connect(context.Background(), os.Getenv("DB_URL"))
	if err != nil {
		log.Fatal("Unable to connect to database")
		os.Exit(1)
	}
	return conn
}

func rolesParse(g *geziyor.Geziyor, r *client.Response) {

	conn := createDbConn()

	r.HTMLDoc.Find("div[class='_19a4fyb0 _1mgddud0 _1mgddud4']").Each(func(i int, s *goquery.Selection) {
		if s.Find("a[data-automation='jobTitle']").Text() != "" {

			// To create the ID
			title := s.Find("a[data-automation='jobTitle']").Text()
			company := s.Find("a[data-automation='jobCompany']").Text()
			id := base64.StdEncoding.EncodeToString([]byte(title + company))

			// Location Text
			var locations []string
			var locationText string
			s.Find("article[data-card-type='JobCard']").Each(func(i int, s *goquery.Selection) {
				locations = append(locations, s.Text())
			})
			if len(locations) > 1 {
				locationText = strings.Join(locations, ", ")
			}

			// Link Text
			linkText := fmt.Sprintf("https://www.seek.com.au%s", s.Find("a[data-automation='jobTitle']").AttrOr("href", ""))

			job := Job{
				Id:       id,
				Title:    title,
				Company:  company,
				Salary:   s.Find("span[data-automation='jobSalary']").Text(),
				Location: locationText,
				Link:     linkText,
				Website:  "seek",
			}

			createTableSQL := `
        		CREATE TABLE IF NOT EXISTS jobs (
        		  id text PRIMARY KEY,
        		  title text NOT NULL,
        		  company text NOT NULL,
        		  salary text,
        		  location text NOT NULL,
        		  link text UNIQUE NULLS NOT DISTINCT,
        		  website text NOT NULL, 
        		  scraped_at timestamp NOT NULL,
        		  status text NOT NULL
        		)
      		`
			_, err := conn.Exec(context.Background(), createTableSQL)
			if err != nil {
				// find the error code for failed table creation
				log.Fatal("FAILED TO CREATE TABLE :: ", err)
			}

			rows, err := conn.Query(context.Background(),
				"SELECT link from jobs WHERE title = $1 and company = $2",
				job.Title, job.Company)
			if err != nil {
				log.Fatal(err)
			}
			defer rows.Close()

			insertTableSQL := `
				INSERT INTO jobs (
          			id,
					title, 
					company, 
					salary, 
					location, 
					link, 
					website,
          			scraped_at,
          			status
        		) VALUES ($1, $2, $3, $4, $5, $6, $7, NOW()::TIMESTAMP, 'None')
      		`

			if !rows.Next() {
				_, err := conn.Exec(
					context.Background(),
					insertTableSQL,
					job.Id,
					job.Title,
					job.Company,
					job.Salary,
					job.Location,
					job.Link,
					job.Website,
				)
				if err != nil {
					if err, ok := err.(*pgconn.PgError); ok && err.Code == "23505" {
						fmt.Println("SKIPPED :: ", job.Title, job.Company)
					} else {
						log.Fatal(err)
					}
				}
			}
		}
	})
	if href, ok := r.HTMLDoc.Find("a[title='Next']").Attr("href"); ok {
		g.Get(r.JoinURL(href), rolesParse)
	}
}
