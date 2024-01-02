package cmd

import (
	"context"
	"fmt"
	cdpNetwork "github.com/chromedp/cdproto/network"
	cdp "github.com/chromedp/chromedp"
	"io/ioutil"
	"os"
	"time"
)

type MTeam struct {
	ChromeFilePath string                    `json:"chrome_file_path"`
	Cookie         string                    `json:"cookie"` //domain cookie
	Options        []cdp.ExecAllocatorOption `json:"options"`
	Timeout        time.Duration             `json:"timeout"` //cdp context  timetout
	Proxy          string                    `json:"proxy"`
}

func (m *MTeam) InitOptions() {
	m.Options = []cdp.ExecAllocatorOption{
		//cdp.ExecPath(m.ChromeFilePath),
		cdp.Flag("headless", false),
		cdp.Flag("start-maximized", true),
		//cdp.Flag("disable-infobars", true),//此参数无效
		cdp.Flag("enable-automation", false),
		cdp.ProxyServer(m.Proxy),
		//cdp.Flag("hide-scrollbars", true),
		//cdp.Flag("mute-audio", false),
		//cdp.UserDataDir(""),

		//cdp.WindowSize(1920, 1080), // init with a mobile view
		cdp.UserAgent(`Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36`),
	}
	m.Options = append(cdp.DefaultExecAllocatorOptions[:],
		m.Options...)

}

func (m *MTeam) DownloadListHtmlByCDP(ctx context.Context, url, htmlTag, htmlFilePath string) (src string, err error) {

	//run until to timeout
	err = cdp.Run(
		ctx,
		SetHeaders(map[string]interface{}{"cookie": m.Cookie}),
		cdp.Navigate(url),
	)
	if err != nil {
		XWarning(fmt.Sprintf(`cdp.Navigate error : %v`, err))
		return src, err
	}

	//run until to timeout
	err = cdp.Run(
		ctx,
		cdp.WaitVisible(htmlTag), //by css selector
	)
	if err != nil {
		XWarning(fmt.Sprintf(`util.RunWithTimeOut  error : %v`, err))
		return src, err
	}

	err = cdp.Run(
		ctx,
		cdp.OuterHTML("html", &src),
	)
	if err != nil {
		XWarning(fmt.Sprintf(`cdp.OuterHTML  error : %v`, err))
		return src, err
	}
	ioutil.WriteFile(htmlFilePath, []byte(src), os.ModePerm)
	return src, nil
}
func SetHeaders(headers map[string]interface{}) cdp.Tasks {
	return cdp.Tasks{
		cdpNetwork.Enable(),
		cdpNetwork.SetExtraHTTPHeaders(headers),
	}
}

//@Title: WaitUntil
// @Description: https://github.com/chromedp/chromedp/issues/37

func RunWithTimeOut(ctx *context.Context, timeout time.Duration, tasks cdp.Tasks) cdp.ActionFunc {
	return func(ctx context.Context) error {
		timeoutContext, cancel := context.WithTimeout(ctx, timeout*time.Second)
		defer cancel()
		return tasks.Do(timeoutContext)
	}
}
