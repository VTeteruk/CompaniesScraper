import time
from selenium.common import NoSuchElementException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import re

from settings import BASE_GOOGLE_MAPS_URL, configure_logging, USE_DIRECT_URL, DIRECT_URL
from models.models import Company
from parsers.chrome_parser import ChromeParser

import logging
from tqdm import tqdm

configure_logging()


class GoogleMapsUrlParser(ChromeParser):
    def wait_for_url_change(self) -> str:
        """Waiting until the URL is correctly updated after navigation"""
        wrong_url = self.driver.current_url
        correct_url = wrong_url
        while correct_url == wrong_url:
            correct_url = self.driver.current_url

        return correct_url

    def extract_city_coordinates(self, city: str) -> str:
        self.driver.get(BASE_GOOGLE_MAPS_URL + city.replace(" ", "+"))
        correct_url = self.wait_for_url_change()

        # Extracting and returning the city coordinates from the correct URL
        try:
            return re.findall(r"/@.*/", correct_url)[0]
        except IndexError:
            raise ValueError("City can't be found")

    def generate_google_maps_url(
            self, companies_field: str, city: str,
    ) -> str:
        """Generate url for searching companies with companies_field in the city"""
        if USE_DIRECT_URL:
            return DIRECT_URL
        logging.info(f"Generating url for {companies_field} in {city}...")
        city_coordinates = self.extract_city_coordinates(city=city)

        return BASE_GOOGLE_MAPS_URL + companies_field + city_coordinates


class GoogleMapsParser(GoogleMapsUrlParser):
    def get_sidebar(self) -> WebElement:
        try:
            return self.driver.find_element(By.XPATH, "//div[@role='feed']")
        except NoSuchElementException:
            raise ValueError("Companies' field can't be found")

    def scroll_to_the_end_of_sidebar(self) -> None:
        sidebar = self.get_sidebar()

        while True:
            # Scroll to the end of the side_panel
            sidebar.send_keys(Keys.PAGE_DOWN)
            try:
                # Check if the program reached the end of the sidebar
                self.driver.find_element(By.CLASS_NAME, "HlvSq")
                break
            except NoSuchElementException:
                time.sleep(0.2)
                # Scroll up to prevent freezing
                self.driver.execute_script("arguments[0].scrollTop -= 100;", sidebar)
                time.sleep(0.2)

    def get_companies_blocks(self) -> list[WebElement]:
        return self.driver.find_elements(By.CLASS_NAME, "lI9IFe")

    @staticmethod
    def initialize_company_data(block: WebElement, class_name: str) -> WebElement | None:
        try:
            element = block.find_element(By.CLASS_NAME, class_name)
            return element
        except NoSuchElementException:
            return None

    def create_companies_instance(self, block: WebElement) -> Company:
        company_name = self.initialize_company_data(block, "qBF1Pd")
        company_number = self.initialize_company_data(block, "UsdlK")
        company_website = self.initialize_company_data(block, "lcr4fd")

        return Company(
            name=company_name.text if company_name else None,
            number=company_number.text if company_number else None,
            website=company_website.get_attribute("href")
            if company_website
            else None,
        )

    def extract_google_maps_data(self, google_maps_url: str) -> list[Company]:
        self.driver.get(google_maps_url)

        logging.info("Scrolling to the end of the sidebar...")
        self.scroll_to_the_end_of_sidebar()

        companies = [
            self.create_companies_instance(block)
            for block
            in tqdm(self.get_companies_blocks(), desc="Parsing Google Maps data")
        ]

        return companies
