from parsers.companies_data_parser import CompaniesDataParser
from utilities.saver import save_data_to_excel, save_data_to_csv
from settings import (
    DEFAULT_COMPANIES_FIELD,
    DEFAULT_CITY,
    FILE_PATH_FOR_XLSX,
    FILE_PATH_FOR_CSV,
    INPUT_MODE,
)


def get_user_input() -> tuple[str, str]:
    companies_field_input = input("Enter companies' field: ")
    city_input = input("Enter city: ")
    return (
        companies_field_input if companies_field_input else DEFAULT_COMPANIES_FIELD,
        city_input if city_input else DEFAULT_CITY,
    )


def main() -> None:
    companies_field, city = (
        get_user_input() if INPUT_MODE else (DEFAULT_COMPANIES_FIELD, DEFAULT_CITY)
    )

    parser = CompaniesDataParser()
    try:
        site_url = parser.generate_google_maps_url(
            companies_field=companies_field, city=city
        )
        data = parser.extract_google_maps_data(site_url)
    finally:
        parser.destroy()

    parser.find_owners(data)

    save_data_to_excel(data, file_path=FILE_PATH_FOR_XLSX)
    save_data_to_csv(data, file_path=FILE_PATH_FOR_CSV)


if __name__ == "__main__":
    main()
