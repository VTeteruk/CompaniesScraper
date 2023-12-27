import dataclasses
import os

import pandas as pd


def data_to_data_frame(companies: list[dataclasses]) -> pd.DataFrame:
    data_list = [dataclasses.asdict(company) for company in companies]
    return pd.DataFrame(data_list)


def create_directory_if_not_exist(file_path: str) -> None:
    parent = os.path.dirname(file_path)
    if not os.path.exists(parent):
        os.makedirs(parent)


def save_data_to_csv(companies: list[dataclasses], file_path: str) -> None:
    create_directory_if_not_exist(file_path)

    data_to_data_frame(companies).to_csv(file_path, index=False)


def save_data_to_excel(companies: list[dataclasses], file_path: str) -> None:
    create_directory_if_not_exist(file_path)

    data_to_data_frame(companies).to_excel(file_path, index=False)
