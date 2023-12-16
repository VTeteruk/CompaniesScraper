import dataclasses
import pandas as pd
from selenium import webdriver

from models import RenovationLead


class ChromeParser:
    def __init__(self) -> None:
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'"
        )
        self.driver = webdriver.Chrome(options=options)

    @staticmethod
    def data_to_data_frame(renovation_leads: list[RenovationLead]) -> pd.DataFrame:
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
