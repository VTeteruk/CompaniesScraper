import dataclasses
import os

import pandas as pd


def data_to_data_frame(renovation_leads: list[dataclasses]) -> pd.DataFrame:
    data_list = [dataclasses.asdict(lead) for lead in renovation_leads]
    return pd.DataFrame(data_list)


def save_data_to_csv(renovation_leads: list[dataclasses], file_path: str) -> None:
    # Create the directory if it doesn't exist
    parent = os.path.dirname(file_path)
    if not os.path.exists(parent):
        os.makedirs(parent)

    data_to_data_frame(renovation_leads).to_csv(file_path, index=False)


def save_data_to_excel(renovation_leads: list[dataclasses], file_path: str) -> None:
    # Create the directory if it doesn't exist
    parent = os.path.dirname(file_path)
    if not os.path.exists(parent):
        os.makedirs(parent)

    data_to_data_frame(renovation_leads).to_excel(file_path, index=False)
