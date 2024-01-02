package cmd

import (
	"log"
	"os"
	"strings"
	"time"
)

// @title    XWarning
// @description    warning日志输出
// @param
// @return
func XWarning(content string) {
	log.Printf(content)
	LogWrite(content)
}

// @title    LogWrite
// @description    log信息写入log文件
// @param
// @return
func LogWrite(content string) {
	//使用当前项目路径
	fd, _ := os.OpenFile("log.log", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0644)
	fd_time := time.Now().Format("2006-01-02 15:04:05")
	fd_content := strings.Join([]string{"======", fd_time, "=====", content, "\n"}, "")
	buf := []byte(fd_content)
	fd.Write(buf)
	fd.Close()
}
