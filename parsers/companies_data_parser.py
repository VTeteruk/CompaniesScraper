from parsers.async_owners_parser import AsyncOwnersParser
from parsers.google_maps_parser import GoogleMapsParser


class CompaniesDataParser(GoogleMapsParser, AsyncOwnersParser):
    pass
