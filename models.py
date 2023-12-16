import dataclasses


@dataclasses.dataclass
class BusinessOwner:
    name: str
    role: str
    status: str

    def __str__(self) -> str:
        return f"{self.name} - {self.role} ({self.status})"


@dataclasses.dataclass
class RenovationLead:
    company_name: str
    company_number: str | None
    company_website: str = None
    business_owners: list[BusinessOwner] = None
