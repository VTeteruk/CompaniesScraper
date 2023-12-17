from selenium import webdriver


class ChromeParser:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'"
        )
        self.driver = webdriver.Chrome(options=options)

    def destroy(self) -> None:
        self.driver.close()
        self.driver.quit()
