from selenium import webdriver

from settings import HEADLESS, USER_AGENT


class ChromeParser:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()

        # Disabling the blink features related to automation to prevent detection
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Setting the user-agent for the web browser to mimic a specific client
        options.add_argument(f"user-agent={USER_AGENT}")

        # Hiding useless logging
        options.add_argument("--log-level=3")

        # Checking if the browser should run in headless mode (without GUI)
        if HEADLESS:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)

    def destroy(self) -> None:
        self.driver.close()
        self.driver.quit()
