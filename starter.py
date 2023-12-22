from settings import COMPANIES_FIELD, CITY, FILE_NAME_FOR_XLSX, FILE_NAME_FOR_CSV
from parsers.companies_data_parser import CompaniesDataParser
from utilities.saver import save_data_to_excel, save_data_to_csv


def main(companies_field: str, city: str) -> None:
    parser = CompaniesDataParser()
    site_url = parser.generate_google_maps_url(companies_field=companies_field, city=city)
    data = parser.extract_google_maps_data(site_url)
    parser.find_owners(data)
    parser.destroy()

    save_data_to_excel(data, file_name=FILE_NAME_FOR_XLSX)
    save_data_to_csv(data, file_name=FILE_NAME_FOR_CSV)


if __name__ == "__main__":
    main(COMPANIES_FIELD, CITY)
