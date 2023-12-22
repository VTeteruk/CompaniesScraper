from selenium import webdriver

from settings import HEADLESS, USER_AGENT


class ChromeParser:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            f"user-agent={USER_AGENT}"
        )
        if HEADLESS:
            options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def destroy(self) -> None:
        self.driver.close()
        self.driver.quit()
