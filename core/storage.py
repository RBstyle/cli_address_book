from dataclasses import dataclass, field
from typing import Optional

from views import get_last_id


@dataclass
class Record:
    id: str = field(init=False, repr=True)
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    company: Optional[str] = None
    work_phone: Optional[int] = None
    mobile_phone: Optional[int] = None

    def __post_init__(self):
        self.id = get_last_id() + 1
