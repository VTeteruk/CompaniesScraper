from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from models.models import BusinessOwner, RenovationLead
from parsers.chrome_parser import ChromeParser


class OwnersParser(ChromeParser):
    @staticmethod
    def search_url(company_name: str) -> str:
        return f"https://find-and-update.company-information.service.gov.uk/search?q={company_name.replace(' ', '+')}"

    @staticmethod
    def is_half_similar(string1: str, string2) -> bool:
        string1 = string1.lower()
        string2 = string2.lower()

        return (
            len([word for word in string1.split() if word in string2])
            >= len(string2.split()) / 2
            or len([word for word in string2.split() if word in string1])
            >= len(string1.split()) / 2
        )

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

    def extract_business_owners(self) -> list[BusinessOwner]:
        business_owners: list[BusinessOwner] = []

        try:
            self.driver.find_element(By.ID, "people-tab").click()
        except NoSuchElementException:
            return []

        person_index = 1
        while True:
            try:
                person_block = self.driver.find_element(
                    By.CLASS_NAME, f"appointment-{person_index}"
                )

                person_status_tag_block = person_block.find_element(
                    By.ID, f"officer-status-tag-{person_index}"
                )
                person_role_block = person_block.find_element(
                    By.ID, f"officer-role-{person_index}"
                )

                person_status_tag = person_status_tag_block.text.strip()
                person_role = person_role_block.text.strip()
                person_name = self.extract_person_name(person_block, person_index)

                business_owners.append(
                    BusinessOwner(person_name, person_role, person_status_tag)
                )

                person_index += 1

            except NoSuchElementException:
                break

        return business_owners

    def scrap_business_owners(self, company_name: str) -> list[BusinessOwner]:
        self.driver.get(self.search_url(company_name))

        search_result = self.driver.find_elements(
            By.XPATH, '//a[@title="View company"]'
        )
        if len(search_result) == 0:
            return []

        searched_company_name_link = self.driver.find_elements(
            By.XPATH, '//a[@title="View company"]'
        )[0]
        stripped_searched_company_name = searched_company_name_link.text.strip()

        if self.validate_company_name(stripped_searched_company_name, company_name):
            searched_company_name_link.click()
            return self.extract_business_owners()

    def find_owners(
        self, renovation_leads: list[RenovationLead]
    ) -> list[RenovationLead]:
        for renovation_lead in renovation_leads:
            business_owners = self.scrap_business_owners(renovation_lead.company_name)
            renovation_lead.business_owners = business_owners

        return renovation_leads
