import time
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import re

from settings import BASE_GOOGLE_MAPS_URL
from models.models import RenovationLead
from parsers.chrome_parser import ChromeParser

import logging
from tqdm import tqdm


class GoogleMapsUrlParser(ChromeParser):
    def extract_city_coordinates(self, city: str) -> str:
        self.driver.get(BASE_GOOGLE_MAPS_URL + city.replace(" ", "+"))

        wrong_url = self.driver.current_url
        correct_url = wrong_url
        while correct_url == wrong_url:
            correct_url = self.driver.current_url

        return re.findall(r"/@.*/", correct_url)[0]

    def generate_google_maps_url(
            self,
            companies_field: str,
            city: str,
    ) -> str:
        """Generate url for searching companies with companies_field in the city"""
        logging.info(f"Generating url for {companies_field} in {city}...")
        city_coordinates = self.extract_city_coordinates(city=city)

        return BASE_GOOGLE_MAPS_URL + companies_field + city_coordinates


class GoogleMapsParser(GoogleMapsUrlParser):
    def scroll_to_the_end_of_sidebar(self) -> None:
        side_panel = self.driver.find_element(By.XPATH, "//div[@role='feed']")

        while True:
            side_panel.send_keys(Keys.PAGE_DOWN)
            try:
                self.driver.find_element(By.CLASS_NAME, "HlvSq")
                break
            except NoSuchElementException:
                time.sleep(0.2)
                self.driver.execute_script("arguments[0].scrollTop -= 100;", side_panel)
                time.sleep(0.2)

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

        logging.info("Scrolling to the end of the sidebar...")
        self.scroll_to_the_end_of_sidebar()

        renovation_leads = []

        for block in tqdm(self.get_companies_blocks(), desc="Parsing google maps data"):
            renovation_leads.append(self.create_renovation_lead_instance(block))
        return renovation_leads


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)
