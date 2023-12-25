from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from tqdm import tqdm

from settings import BASE_GOV_URL
from models.models import BusinessOwner, Company
from parsers.chrome_parser import ChromeParser


class OwnersParser(ChromeParser):
    @staticmethod
    def search_url(company_name: str) -> str:
        return f"{BASE_GOV_URL}search?q={company_name.replace(' ', '+')}"

    @staticmethod
    def is_half_similar(string1: str, string2) -> bool:
        words1 = set(string1.lower().split())
        words2 = set(string2.lower().split())
        intersection = words1.intersection(words2)

        return len(intersection) >= min(len(words1), len(words2)) / 2

    @staticmethod
    def extract_person_name(person_block: WebElement, person_index: int) -> str:
        return (
            person_block.find_element(
                By.ID, f"officer-name-{person_index}"
            ).find_element(By.TAG_NAME, "a")
        ).text.strip()

    def validate_company_name(
        self, searched_company_name: str, real_company_name: str
    ) -> bool:
        return self.is_half_similar(searched_company_name, real_company_name)

    def extract_business_owners(self) -> list[str]:
        business_owners: list[str] = []

        try:
            self.driver.find_element(By.ID, "people-tab").click()
        except NoSuchElementException:
            return []

        person_index = 1
        while True:
            try:
                # Locating elements representing a person block
                person_block = self.driver.find_element(
                    By.CLASS_NAME, f"appointment-{person_index}"
                )

                person_status_tag_block = person_block.find_element(
                    By.ID, f"officer-status-tag-{person_index}"
                )
                person_role_block = person_block.find_element(
                    By.ID, f"officer-role-{person_index}"
                )

                # Extracting information about the person
                person_status_tag = person_status_tag_block.text.strip()
                person_role = person_role_block.text.strip()
                person_name = self.extract_person_name(person_block, person_index)

                business_owners.append(
                    str(BusinessOwner(person_name, person_role, person_status_tag))
                )

                person_index += 1
            except NoSuchElementException:
                break

        return business_owners

    def scrap_business_owners(self, company_name: str) -> list[str]:
        self.driver.get(self.search_url(company_name))

        search_result = self.driver.find_elements(
            By.XPATH, '//a[@title="View company"]'
        )

        if not len(search_result):
            return []

        searched_company_name_link = self.driver.find_elements(
            By.XPATH, '//a[@title="View company"]'
        )[0]
        stripped_searched_company_name = searched_company_name_link.text.strip()

        if self.validate_company_name(stripped_searched_company_name, company_name):
            searched_company_name_link.click()
            return self.extract_business_owners()
        return []

    def find_owners(
        self, companies: list[Company]
    ) -> list[Company]:
        for company in tqdm(companies, desc="Parsing owners' data"):
            business_owners = self.scrap_business_owners(company.name)
            company.owners = business_owners

        return companies
