from parsers.companies_data_parser import CompaniesDataParser
from utilities.saver import save_data_to_excel, save_data_to_csv


def main(site_url: str) -> None:
    parser = CompaniesDataParser()
    data = parser.extract_google_maps_data(site_url)
    parser.find_owners(data)
    parser.destroy()

    save_data_to_excel(data, file_name="renovation_leads")
    save_data_to_csv(data, file_name="renovation_leads")


if __name__ == "__main__":
    main(
        site_url="https://www.google.com/maps/search/"
        "renovation/@52.583251,-0.2907134,12.05z?entry=ttu"
    )
