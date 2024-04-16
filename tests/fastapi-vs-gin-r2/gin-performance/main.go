package main

import (
	"log"
	"strconv"
	"time"

	"database/sql"

	"github.com/google/uuid"
	_ "github.com/lib/pq"

	"github.com/gin-gonic/gin"
)

var db *sql.DB

func init() {
	var err error
	connStr := "host='localhost' user='postgres' dbname='testing' sslmode=disable"
	db, err = sql.Open("postgres", connStr)
	if err != nil {
		log.Fatal(err)
	}
}

type User struct {
	ID       uuid.UUID `json:"id"`
	Username string    `json:"username"`
	Rank	 int       `json:"rank"`
	CreatedAt  time.Time `json:"created_at"`
}


type Item struct {
	Username  string    `json:"username"`
	ID        int       `json:"id"`
	Timestamp string    `json:"timestamp"`
}

func main() {
	r := gin.Default()

	r.GET("/", func(c *gin.Context) {
		var data []Item
		for i := 0; i < 1000; i++ {
			timestamp := time.Now().Format("2006-01-02T15:04:05.999999")
			data = append(data, Item{
				Username:  "user" + strconv.Itoa(i),
				ID:        i,
				Timestamp: timestamp,
			})
		}
		c.Header("Server", "Gin")
		c.JSON(200, data)
	})

	r.GET("/status", func(c *gin.Context) {
		c.Status(200)
	})

	r.GET("/db_obj", func(c *gin.Context) {
		rows, err := db.Query("select * from users")
		if err != nil {
			log.Fatal(err)
		}
		defer rows.Close()

		var users []User
		for rows.Next() {
			var user User
			err := rows.Scan(&user.ID, &user.Username, &user.Rank, &user.CreatedAt)
			if err != nil {
				log.Fatal(err)
			}
			users = append(users, user)
		}

		c.JSON(200, users)
	})

		

	r.GET("/db_json", func(c *gin.Context) {
		var jsonString string
		err := db.QueryRow("select json_agg(c) from (select * from users) as c").Scan(&jsonString)
		if err != nil {
			log.Fatal(err)
		}

		c.Data(200, "application/json; charset=utf-8", []byte(jsonString))
	})

	r.Run(":8001")
}
