import dataclasses
import time
import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement


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

    def create_renovation_leads_instances(
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
                self.create_renovation_leads_instances(block)
            )

        return renovation_leads


class OwnersParser(ChromeParser):
    pass


if __name__ == "__main__":
    parser = GoogleMapsParser()
    data = parser.main(
            "https://www.google.com/maps/search/"
            "renovation/@54.5540137,-1.546097,10z?entry=ttu"
        )
    parser.save_data_to_excel(data, "renovation_leads")
    parser.save_data_to_csv(data, "renovation_leads")
    parser.destroy()
