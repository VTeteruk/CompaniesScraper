from parsers.companies_data_parser import CompaniesDataParser
from utilities.saver import save_data_to_excel, save_data_to_csv
from settings import (
    DEFAULT_COMPANIES_FIELD,
    DEFAULT_CITY,
    FILE_PATH_FOR_XLSX,
    FILE_PATH_FOR_CSV,
    INPUT_MODE
)


def main(companies_field: str, city: str) -> None:
    parser = CompaniesDataParser()
    site_url = parser.generate_google_maps_url(companies_field=companies_field, city=city)
    data = parser.extract_google_maps_data(site_url)
    parser.find_owners(data)
    parser.destroy()

    save_data_to_excel(data, file_path=FILE_PATH_FOR_XLSX)
    save_data_to_csv(data, file_path=FILE_PATH_FOR_CSV)


if __name__ == "__main__":
    if INPUT_MODE:
        companies_field_input = input("Enter companies' field: ")
        city_input = input("Enter city: ")
        main(
            companies_field=companies_field_input
            if companies_field_input
            else DEFAULT_COMPANIES_FIELD,

            city=city_input if city_input else DEFAULT_CITY
        )
    else:
        main(DEFAULT_COMPANIES_FIELD, DEFAULT_CITY)
