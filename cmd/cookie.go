package cmd

import (
	"fmt"
	"github.com/zellyn/kooky/browser/chrome"
	"log"
	"strings"
)

func ReadDomainCookieFromChrome(domain, cookieFilePath string) (cook string) {

	cookies, err := chrome.ReadCookies(cookieFilePath)
	if err != nil {
		log.Fatal(err)
	}
	cookieData := []string{}
	for _, cookie := range cookies {
		if cookie.Domain == domain {
			cookieData = append(cookieData, fmt.Sprintf("%v=%v", cookie.Name, cookie.Value))
		}
	}

	cook = strings.Join(cookieData, ";")

	return

}
