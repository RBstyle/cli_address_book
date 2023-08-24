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

    def str_dict(self):
        return json.dumps(asdict(self))

    def get_field_names(self) -> dict:
        """Return dict of field names excluding "id" {index number: "field_name", ...}"""
        field_names = self.__dict__
        del field_names["id"]
        return dict(enumerate(field_names, start=1))

    def get_verbose_field_names(self) -> dict:
        """Return dict of verbose field names excluding "id" {index number: "verbose_name"}
        (Record attributes should be: id, last_name, first_name, patronymic, company, work_phone, mobile_phone)
        """
        fields = {
            "last_name": "Имя",
            "first_name": "Фамилия",
            "patronymic": "Отчество",
            "company": "Название компании",
            "work_phone": "Рабочий телефон",
            "mobile_phone": "Мобильный телефон",
        }
        field_names = self.get_field_names()
        for index, field_name in field_names.items():
            verbose_name = fields.get(field_names[index])
            if verbose_name:
                field_names[index] = verbose_name
        return field_names
