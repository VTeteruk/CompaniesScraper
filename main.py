import logging

from parsers.async_owners_parser import AsyncOwnersParser
from parsers.google_maps_parser import GoogleMapsParser
from utilities.saver import save_data_to_excel, save_data_to_csv
import settings

settings.configure_logging()


def get_user_input() -> tuple[str, str]:
    while True:
        companies_field_input = input(f"Enter companies' field: ")
        if not companies_field_input or not companies_field_input.isalpha():
            logging.info("Please enter a valid companies' filed")
            continue
        break
    while True:
        city_input = input(f"Enter city: ")
        if not city_input or not city_input.isalpha():
            logging.info("Please enter a valid city")
            continue
        break
    return companies_field_input, city_input


def main() -> None:
    companies_field, city = None, None
    if settings.INPUT_MODE:
        if "y" in input(f"Use default variables ({settings.DEFAULT_COMPANIES_FIELD}, {settings.DEFAULT_CITY}) (y/n): ").lower():
            companies_field, city = settings.DEFAULT_COMPANIES_FIELD, settings.DEFAULT_CITY
        else:
            companies_field, city = get_user_input()

    for _ in range(settings.TRIES_FOR_WEBSITE):
        with GoogleMapsParser() as parser:
            site_url = parser.generate_google_maps_url(
                companies_field=companies_field, city=city
            )
            data = parser.extract_google_maps_data(site_url)
            if any([company.website for company in data]):
                break
            logging.info("Websites weren't parsed. Restarting...")

    if not data:
        logging.info("Something went wrong...")

    logging.info("Looking for owners...")
    parser = AsyncOwnersParser()
    parser.find_owners(data)

    logging.info("Saving data...")
    if not settings.PYTHON_LISTS_IN_RESULTS:
        for company in data:
            company.owners = "; ".join(company.owners) if company.owners else ""
    save_data_to_excel(data, file_path=settings.FILE_PATH_FOR_XLSX)
    save_data_to_csv(data, file_path=settings.FILE_PATH_FOR_CSV)


if __name__ == "__main__":
    main()
