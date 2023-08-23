import json
from dataclasses import dataclass, field, asdict
from typing import Optional

from core.utils import get_last_id


@dataclass
class Record:
    id: int = field(init=False, repr=True)
    last_name: Optional[str] = None
    first_name: Optional[str] = None
    patronymic: Optional[str] = None
    company: Optional[str] = None
    work_phone: Optional[int] = None
    mobile_phone: Optional[int] = None

    def __post_init__(self):
        self.id = get_last_id() + 1

    def dict(self):
        return {k: v for k, v in asdict(self).items()}

    def str_dict(self):
        return json.dumps(asdict(self))
