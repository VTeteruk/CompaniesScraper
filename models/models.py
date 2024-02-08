import dataclasses


@dataclasses.dataclass
class BusinessOwner:
    name: str
    role: str
    status: str

    def __str__(self) -> str:
        return f"{self.name} - {self.role} ({self.status})"


@dataclasses.dataclass
class Company:
    name: str
    searched_company_name: str = None
    number: str = None
    website: str = None
    owners: list[BusinessOwner] = None
