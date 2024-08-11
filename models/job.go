package models

type Job struct {
	Id       string `json:"id"`
	Title    string `json:"title"`
	Company  string `json:"company"`
	Salary   string `json:"salary"`
	Location string `json:"location"`
	Link     string `json:"link"`
	Website  string `json:"website"`
}
