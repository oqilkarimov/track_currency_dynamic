from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Self


# noqa: C0103
# pylint: disable=invalid-name
@dataclass
class CBRValute:
    ID: str
    NumCode: str
    CharCode: str
    Nominal: int
    Name: str
    Value: float
    Previous: float


# noqa: C0103
# pylint: disable=invalid-name
@dataclass
class CBRResponse:
    Date: datetime
    PreviousDate: datetime
    PreviousURL: str
    Timestamp: datetime
    Valute: List[CBRValute] = field(default_factory=lambda: [])

    @classmethod
    def from_dict(cls, data: Dict) -> Self:
        valute: dict = data.pop("Valute", None)
        cbr_response_instance = cls(**data)
        for value in valute.values():
            cbr_response_instance.Valute.append(CBRValute(**value))
        return cbr_response_instance
