package cmd

import (
	"encoding/json"
	"fmt"
	"github.com/PuerkitoBio/goquery"
	"io/ioutil"
	"os"
	"strings"
)

func ParseMteamList(source, jsonFilePath string) {
	soup, _ := goquery.NewDocumentFromReader(strings.NewReader(source))
	datas := map[string][]string{}
	domain := "https://kp.m-team.cc/"
	soup.Find(`tr>td[class='torrentimg']>a[href*='details']:nth-child(1)`).Each(func(i int, a *goquery.Selection) {
		data := []string{}

		title, _ := a.Attr("title")
		data = append(data, title)

		href, _ := a.Attr("href")
		href = fmt.Sprintf(`%s%s`, domain, href)

		src, _ := a.Find("img").Attr("src")
		data = append(data, src)

		datas[href] = data
	})
	//fmt.Printf("%v\n", data)
	jsonData, _ := json.MarshalIndent(datas, "", "\t")
	ioutil.WriteFile(jsonFilePath, jsonData, os.ModePerm)
}
