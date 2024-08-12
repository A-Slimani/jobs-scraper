package parsers

import (
	"encoding/base64"
	"fmt"
	"strings"

	"job-scraper/models"

	"github.com/PuerkitoBio/goquery"
	"github.com/geziyor/geziyor"
	"github.com/geziyor/geziyor/client"
)

func SeekRolesParse(g *geziyor.Geziyor, r *client.Response) {
	// gets the list of cards
	r.HTMLDoc.Find("article[data-testid='job-card']").Each(func(i int, s *goquery.Selection) {
		if s.Find("a[data-automation='jobTitle']").Text() != "" {

			// To create the ID
			title := s.Find("a[data-automation='jobTitle']").Text()
			company := s.Find("a[data-automation='jobCompany']").Text()
			id := base64.StdEncoding.EncodeToString([]byte(title + company))

			// Location Text
			var locations []string
			var locationText string
			s.Find("a[data-automation='jobLocation']").Each(func(i int, s *goquery.Selection) {
				locations = append(locations, s.Text())
			})
			if len(locations) > 1 {
				locationText = strings.Join(locations, ", ")
			}

			// Link Text
			linkText := fmt.Sprintf("https://www.seek.com.au%s", s.Find("a[data-automation='jobTitle']").AttrOr("href", ""))

			job := models.Job{
				Id:       id,
				Title:    title,
				Company:  company,
				Salary:   s.Find("span[data-automation='jobSalary']").Text(),
				Location: locationText,
				Link:     linkText,
				Website:  "Seek",
				Status:   "None",
			}

			g.Exports <- job

		}
	})
	if href, ok := r.HTMLDoc.Find("a[title='Next']").Attr("href"); ok {
		g.Get(r.JoinURL(href), SeekRolesParse)
	}
}
