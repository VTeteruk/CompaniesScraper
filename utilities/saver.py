import dataclasses
import pandas as pd


def data_to_data_frame(renovation_leads: list[dataclasses]) -> pd.DataFrame:
    data_list = [dataclasses.asdict(lead) for lead in renovation_leads]
    return pd.DataFrame(data_list)


def save_data_to_csv(
    renovation_leads: list[dataclasses], file_name: str
) -> None:
    data_to_data_frame(renovation_leads).to_csv(
        f"{file_name}.csv", index=False
    )


def save_data_to_excel(
    renovation_leads: list[dataclasses], file_name: str
) -> None:
    data_to_data_frame(renovation_leads).to_excel(
        f"{file_name}.xlsx", index=False
    )
