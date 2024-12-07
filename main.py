import logging

from parsers.companies_data_parser import CompaniesDataParser
from utilities.saver import save_data_to_excel, save_data_to_csv
import settings

settings.configure_logging()


def get_user_input() -> tuple[str, str]:
    companies_field_input = input(f"Enter companies' field ({settings.DEFAULT_COMPANIES_FIELD}): ")
    city_input = input(f"Enter city ({settings.DEFAULT_CITY}): ")
    return (
        companies_field_input if companies_field_input else settings.DEFAULT_COMPANIES_FIELD,
        city_input if city_input else settings.DEFAULT_CITY,
    )


def main() -> None:
    companies_field, city = None, None
    if settings.INPUT_MODE:
        companies_field, city = get_user_input()

    with CompaniesDataParser() as parser:
        site_url = parser.generate_google_maps_url(
            companies_field=companies_field, city=city
        )
        data = parser.extract_google_maps_data(site_url)

    logging.info("Looking for owners...")
    parser.find_owners(data)

    logging.info("Saving data...")
    if not settings.PYTHON_LISTS_IN_RESULTS:
        for company in data:
            company.owners = "; ".join(company.owners) if company.owners else ""
    save_data_to_excel(data, file_path=settings.FILE_PATH_FOR_XLSX)
    save_data_to_csv(data, file_path=settings.FILE_PATH_FOR_CSV)


if __name__ == "__main__":
    main()
