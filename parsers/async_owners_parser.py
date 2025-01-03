import asyncio
import aiohttp
from bs4 import BeautifulSoup

from models.models import Company, BusinessOwner
from settings import BASE_GOV_URL, USER_AGENT


class AsyncOwnersParser:
    @staticmethod
    def search_url(company_name: str) -> str:
        return (
            f"{BASE_GOV_URL}search?q={company_name.replace(' ', '+').replace('&', '%26')}"
        )

    @staticmethod
    def is_half_similar(string1: str, string2: str) -> bool:
        words1 = set(string1.lower().split())
        words2 = set(string2.lower().split())
        intersection = words1.intersection(words2)

        return len(intersection) >= min(len(words1), len(words2)) / 2

    @staticmethod
    def extract_business_owners(soup) -> list[str]:
        business_owners = []

        person_index = 1
        while (
            person_block := soup.find("div", {"class": f"appointment-{person_index}"})
        ) is not None:
            try:
                person_status_tag = person_block.find(
                    "span", {"id": f"officer-status-tag-{person_index}"}
                )
                person_role = person_block.find(
                    "dd", {"id": f"officer-role-{person_index}"}
                ).text.strip()
                person_name = person_block.find(
                    "span", {"id": f"officer-name-{person_index}"}
                ).text.strip()

                business_owners.append(
                    str(BusinessOwner(
                        name=person_name,
                        role=person_role,
                        status=person_status_tag.text.strip() if person_status_tag else "UNKNOWN"
                    ))
                )

                person_index += 1
            except AttributeError:
                break

        return business_owners

    @staticmethod
    async def fetch_url_content(session, url: str) -> str:
        try:
            async with session.get(url) as response:
                return await response.text()
        except Exception as e:
            print(f"Error getting response text: {e}")
            return ""

    async def get_owners(self, session, company_url: str) -> list[str]:
        text_response = await self.fetch_url_content(session, company_url)
        if not text_response:
            return []

        soup = BeautifulSoup(text_response, "html.parser")
        return self.extract_business_owners(soup)

    async def look_for_owners(self, session, company: Company) -> None:
        url = self.search_url(company.name)
        text_response = await self.fetch_url_content(session, url)

        if not text_response:
            company.owners = []
            return

        soup = BeautifulSoup(text_response, "html.parser")
        searched_company_name_link = soup.find("a", {"title": "View company"})

        if not searched_company_name_link or not self.is_half_similar(
            searched_company_name_link.text.strip(), company.name
        ):
            company.owners = []
        else:
            company_url = (
                f"{BASE_GOV_URL[:-1]}{searched_company_name_link.get('href')}/officers"
            )
            company.owners = await self.get_owners(session, company_url)
            company.searched_company_name = searched_company_name_link.text.strip()

    async def create_coroutines(self, companies: list[Company]) -> None:
        headers = {"user-agent": USER_AGENT}

        async with aiohttp.ClientSession(headers=headers) as session:
            coroutines = [self.look_for_owners(session, company) for company in companies]
            await asyncio.gather(*coroutines)

    def find_owners(self, companies: list[Company]) -> None:
        asyncio.run(self.create_coroutines(companies=companies))
