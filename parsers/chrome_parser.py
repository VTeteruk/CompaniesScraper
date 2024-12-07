from __future__ import annotations
from selenium import webdriver
import settings


class ChromeParser:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()

        # Disabling the blink features related to automation to prevent detection
        options.add_argument("--disable-blink-features=AutomationControlled")

        # Setting the user-agent for the web browser to mimic a specific client
        options.add_argument(f"user-agent={settings.USER_AGENT}")

        # Hiding useless logging
        options.add_argument("--log-level=3")

        # Checking if the browser should run in headless mode (without GUI)
        if settings.HEADLESS:
            options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=options)

    def __enter__(self) -> ChromeParser:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.destroy_driver()

    def destroy_driver(self) -> None:
        self.driver.close()
        self.driver.quit()
