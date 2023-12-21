import time
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from models.models import RenovationLead
from parsers.chrome_parser import ChromeParser


class GoogleMapsParser(ChromeParser):
    def scroll_to_the_end_of_sidebar(self) -> None:
        side_panel = self.driver.find_element(By.XPATH, "//div[@role='feed']")

        while True:
            self.driver.execute_script("arguments[0].scrollTop += 500;", side_panel)
            time.sleep(0.2)
            try:
                self.driver.find_element(By.CLASS_NAME, "HlvSq")
                break
            except NoSuchElementException:
                pass

    def get_companies_blocks(self) -> list[WebElement]:
        return self.driver.find_elements(By.CLASS_NAME, "lI9IFe")

    @staticmethod
    def initialize_company_data(block, class_name: str) -> WebElement | None:
        try:
            element = block.find_element(By.CLASS_NAME, class_name)
            return element
        except NoSuchElementException:
            return None

    def create_renovation_lead_instance(self, block: WebElement) -> RenovationLead:
        company_name = self.initialize_company_data(block, "qBF1Pd")
        company_number = self.initialize_company_data(block, "UsdlK")
        company_website = self.initialize_company_data(block, "lcr4fd")

        return RenovationLead(
            company_name=company_name.text if company_name else None,
            company_number=company_number.text if company_number else None,
            company_website=company_website.get_attribute("href")
            if company_website
            else None,
        )

    def extract_google_maps_data(self, google_maps_url: str) -> list[RenovationLead]:
        self.driver.get(google_maps_url)

        self.scroll_to_the_end_of_sidebar()

        renovation_leads = []

        for block in self.get_companies_blocks():
            renovation_leads.append(self.create_renovation_lead_instance(block))
        return renovation_leads
