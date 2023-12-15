import dataclasses
import time

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By


@dataclasses.dataclass
class RenovationLead:
    company_name: str
    company_number: str | None
    company_website: str = None
    business_owners: list[str] = None


class ChromeParser:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)


class GoogleMapsParser(ChromeParser):
    def scroll_to_the_end_of_sidebar(self) -> None:
        side_panel = self.driver.find_element(By.XPATH, "//div[@role='feed']")

        while True:
            self.driver.execute_script("arguments[0].scrollTop += 500;", side_panel)
            time.sleep(0.1)
            try:
                self.driver.find_element(By.CLASS_NAME, "HlvSq")
                break
            except NoSuchElementException:
                pass

    def main(self, google_maps_url: str) -> list[RenovationLead]:
        self.driver.get(google_maps_url)

        self.scroll_to_the_end_of_sidebar()


class OwnersParser(ChromeParser):
    pass
