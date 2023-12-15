from selenium import webdriver


class ChromeParser:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)


class GoogleMapsParser(ChromeParser):
    pass


class OwnersParser(ChromeParser):
    pass
