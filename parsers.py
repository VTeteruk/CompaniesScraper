import dataclasses
import time
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from models import RenovationLead, BusinessOwner


class ChromeParser:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        self.driver = webdriver.Chrome(options=options)

    @staticmethod
    def data_to_data_frame(
            renovation_leads: list[RenovationLead]
    ) -> pd.DataFrame:
        data_list = [dataclasses.asdict(lead) for lead in renovation_leads]
        return pd.DataFrame(data_list)

    def save_data_to_csv(
            self, renovation_leads: list[RenovationLead], file_name: str
    ) -> None:
        self.data_to_data_frame(renovation_leads).to_csv(
            f"{file_name}.csv", index=False
        )

    def save_data_to_excel(
            self, renovation_leads: list[RenovationLead], file_name: str
    ) -> None:
        self.data_to_data_frame(renovation_leads).to_excel(
            f"{file_name}.xlsx", index=False
        )

    def destroy(self) -> None:
        self.driver.close()
        self.driver.quit()


class GoogleMapsParser(ChromeParser):
    def scroll_to_the_end_of_sidebar(self) -> None:
        side_panel = self.driver.find_element(By.XPATH, "//div[@role='feed']")

        while True:
            self.driver.execute_script(
                "arguments[0].scrollTop += 500;", side_panel
            )
            time.sleep(0.1)
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
            element = block.find_element(
                By.CLASS_NAME, class_name
            )
            return element
        except NoSuchElementException:
            return None

    def create_renovation_lead_instance(
            self, block: WebElement
    ) -> RenovationLead:
        company_name = self.initialize_company_data(block, "qBF1Pd")
        company_number = self.initialize_company_data(block, "UsdlK")
        company_website = self.initialize_company_data(block, "lcr4fd")

        return RenovationLead(
            company_name=company_name.text if company_name else None,
            company_number=company_number.text if company_number else None,
            company_website=company_website.get_attribute(
                "href"
            ) if company_website else None
        )

    def main(self, google_maps_url: str) -> list[RenovationLead]:
        self.driver.get(google_maps_url)

        self.scroll_to_the_end_of_sidebar()

        renovation_leads = []

        for block in self.get_companies_blocks():
            renovation_leads.append(
                self.create_renovation_lead_instance(block)
            )

        return renovation_leads


class OwnersParser(ChromeParser):
    @staticmethod
    def search_url(company_name: str) -> str:
        return f"https://find-and-update.company-information.service.gov.uk/search?q={company_name.replace(' ', '+')}"

    @staticmethod
    def is_half_similar(string1: str, string2) -> bool:
        string1 = string1.lower()
        string2 = string2.lower()

        return (len([word for word in string1.split() if word in string2]) >= len(string2.split()) / 2
                or
                len([word for word in string2.split() if word in string1]) >= len(string1.split()) / 2)

    @staticmethod
    def extract_person_name(person_block: WebElement, person_index: int) -> str:
        return (person_block
                .find_element(By.ID, f"officer-name-{person_index}").find_element(By.TAG_NAME, "a")).text.strip()

    def validate_company_name(self, searched_company_name: str, real_company_name: str) -> bool:
        return self.is_half_similar(searched_company_name, real_company_name)

    def extract_business_owners(self) -> list[BusinessOwner]:
        business_owners: list[BusinessOwner] = []

        try:
            self.driver.find_element(By.ID, "people-tab").click()
        except NoSuchElementException:
            return []

        person_index = 1
        while True:
            try:
                person_block = self.driver.find_element(By.CLASS_NAME, f"appointment-{person_index}")

                person_status_tag_block = person_block.find_element(By.ID, f"officer-status-tag-{person_index}")
                person_role_block = person_block.find_element(By.ID, f"officer-role-{person_index}")

                person_status_tag = person_status_tag_block.text.strip()
                person_role = person_role_block.text.strip()
                person_name = self.extract_person_name(person_block, person_index)

                business_owners.append(BusinessOwner(person_name, person_role, person_status_tag))

                person_index += 1

            except NoSuchElementException:
                break

        return business_owners

    def scrap_business_owners(self, company_name: str) -> list[BusinessOwner]:
        self.driver.get(self.search_url(company_name))

        search_result = self.driver.find_elements(By.XPATH, '//a[@title="View company"]')
        if len(search_result) == 0:
            return []

        searched_company_name_link = self.driver.find_elements(By.XPATH, '//a[@title="View company"]')[0]
        stripped_searched_company_name = searched_company_name_link.text.strip()

        if self.validate_company_name(stripped_searched_company_name, company_name):
            searched_company_name_link.click()
            return self.extract_business_owners()

    def find_owners(self, renovation_leads: list[RenovationLead]) -> list[RenovationLead]:

        for renovation_lead in renovation_leads:
            business_owners = self.scrap_business_owners(renovation_lead.company_name)
            renovation_lead.business_owners = business_owners

        return renovation_leads


if __name__ == "__main__":
    google_maps_parser = GoogleMapsParser()
    data = google_maps_parser.main(
            "https://www.google.com/maps/search/"
            "renovation/@52.583251,-0.2907134,12.05z?entry=ttu"
        )
    owners_parser = OwnersParser()
    owners_parser.find_owners(data)

    google_maps_parser.save_data_to_excel(data, "renovation_leads")
    google_maps_parser.save_data_to_csv(data, "renovation_leads")
    google_maps_parser.destroy()
