package utils

import (
	"context"
	"log"
	"os"
	"reflect"

	"scraper-jobs/models"

	"github.com/jackc/pgx/v5"
	"github.com/joho/godotenv"
	"github.com/pocketbase/pocketbase"
	"github.com/pocketbase/pocketbase/forms"
	"github.com/pocketbase/pocketbase/models"
)

func CreateDbConn() *pgx.Conn {
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

func StructToMap(obj interface{}) map[string]interface{} {
	val := reflect.ValueOf(obj)
	typ := reflect.TypeOf(obj)
	data := make(map[string]interface{})

	for i := 0; i < val.NumField(); i++ {
		data[typ.Field(i).Name] = val.Field(i).Interface()
	}

	return data
}

func UpdateDb(app *pocketbase.PocketBase, job models.Job) {
	collection, err := app.Dao().FindCollectionByNameOrId("jobs")
	if err != nil {
		log.Fatal(err)
	}

	record := models.NewRecord(collection)

	form := forms.NewRecordUpsert(app, record)

	data := StructToMap(job)

	if err := form.LoadData(data); err != nil {
		log.Fatal(err)
	}

}
