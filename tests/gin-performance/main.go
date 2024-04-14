package main

import (
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
)

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

	r.Run(":8001")
}
