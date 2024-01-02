package cmd

import (
	"context"
	"fmt"
	cdp "github.com/chromedp/chromedp"
	"os"
	"path/filepath"
	"time"
)

func CheckIn() {

	dir, _ := os.UserHomeDir()
	LocalAppData := filepath.Join(dir, "/AppData/Local")
	cookiesFile := filepath.Join(LocalAppData, "/Google/Chrome/User Data/Default/Network/Cookies")
	println(cookiesFile)
	cookie := ReadDomainCookieFromChrome(".m-team.cc", cookiesFile)
	cookie = fmt.Sprintf(`%s;%s`, cookie, ReadDomainCookieFromChrome("kp.m-team.cc", cookiesFile))
	m := &MTeam{
		//ChromeFilePath: "D:\\Portable\\chrome-win\\chrome.exe",
		Cookie:  cookie,
		Timeout: time.Duration(60 * 3),
		Proxy:   "http://127.0.0.1:1080",
	}

	m.InitOptions()

	execAllocator, cancel := cdp.NewExecAllocator(
		context.Background(),
		//cdp.WithDebugf(log.Printf),
		m.Options...,
	)
	defer cancel()

	ctx, cancel := cdp.NewContext(execAllocator)
	defer cancel()

	tctx, cancel := context.WithTimeout(ctx, m.Timeout*time.Second)
	defer cancel()

	visibleTag := "table.torrents"
	rootPath, _ := os.Getwd()
	for page := 0; page < 3; page++ {
		adultURL := fmt.Sprintf(`https://kp.m-team.cc/adult.php?inclbookmarked=0&incldead=1&spstate=0&cat410=1&cat429=1&page=%d`, page)
		source, err := m.DownloadListHtmlByCDP(tctx, adultURL, visibleTag, filepath.Join(rootPath, "temp", fmt.Sprintf("page_%d.json", page)))
		if err != nil {
			XWarning(fmt.Sprintf("cdpc.DownloadHtmlByCDP error : %v", err))
			continue
		}

		ParseMteamList(source, filepath.Join(rootPath, "temp", fmt.Sprintf("page_%d.json", page)))

		time.Sleep(1 * time.Second)
	}
}
