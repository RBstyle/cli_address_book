from dataclasses import dataclass, field

from core.utils import get_last_id, border_msg


@dataclass
class Record:
    """
    Датакласс записи в телефонной книге. При создании экземпляра класса

    в генерируется ID и поля заполняются дефолтными значениями

    Атрибуты
    ----------
    id: int
        ID записи, генерирутся при создании экземпляра класса
    last_name: str = None
        Поле "Имя". При создании экземпляра класса получает значение None
    first_name: str = None
        Поле "Фамилия". При создании экземпляра класса получает значение None
    patronymic: str = None
        Поле "Отчество". При создании экземпляра класса получает значение None
    company: str = None
        Поле "Название компании". При создании экземпляра класса получает значение None
    work_phone: int = None
        Поле "Рабочий телефон". При создании экземпляра класса получает значение None
    mobile_phone: int = None
        Поле "Мобильный телефон". При создании экземпляра класса получает значение None

    Методы
    -------
    __post_init__()
        Генерирует ID для новой записи(последний существующий + 1)
    str_validator(attribute: str, default_data=None)
        Валидация значения строковых полей
    phone_validator(attribute: str, default_data=None)
        Валидация полей номеров телефонов
    get_field_names()
        Возвращает словарь имён атрибутов и соответвующих пунктов навигации,
        кроме атрибута ID {index number: "field_name", ...}
    get_verbose_field_names()
        Возвращает словарь читабельных имён атрибутов и соответвующих пунктов навигации,
        кроме атрибута ID {index number: "verbose_name", ...}
    readeble_view()
        Приведение записи из телефонной книги в читабельный вид
    """

    id: int = field(init=False, repr=True)
    last_name: str = None
    first_name: str = None
    patronymic: str = None
    company: str = None
    work_phone: int = None
    mobile_phone: int = None

    def __post_init__(self):
        """Генерирует ID для новой записи(последний существующий + 1)"""
        self.id = get_last_id() + 1

    def str_validator(self, attribute: str, default_data=None):
        """Валидация значения строковых полей"""
        if len(getattr(self, attribute)) > 50 or not getattr(self, attribute).isalpha():
            setattr(self, attribute, default_data)
            return border_msg(
                "Поле должно содержать только буквы и быть короче 50 символов!"
            )
        return True

    def phone_validator(self, attribute: str, default_data=None):
        """Валидация полей номеров телефонов"""
        number = getattr(self, attribute).replace("+", "")
        if (
            len(number) > 11
            or not number.isdigit()
            or not str(number).startswith(("7", "8"))
        ):
            setattr(self, attribute, default_data)
            return border_msg("Введите телефон в формате +7********** или 8**********")
        return True

    def get_field_names(self) -> dict:
        """Возвращает словарь имён атрибутов и соответвующих пунктов навигации,
        кроме атрибута ID {index number: "field_name", ...}"""
        field_names = self.__dict__.copy()
        field_names.pop("id", None)
        return dict(enumerate(field_names, start=1))

    def get_verbose_field_names(self) -> dict:
        """Возвращает словарь читабельных имён атрибутов и соответвующих пунктов навигации,
        кроме атрибута ID {index number: "verbose_name", ...}
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

        for index in field_names.keys():
            verbose_name = fields.get(field_names[index])
            if verbose_name:
                field_names[index] = verbose_name
        return field_names

    def readeble_view(self) -> str:
        """Приведение записи из телефонной книги в читабельный вид"""
        result = f"""
ID: {self.id}
Имя: {self.last_name}
Фамилия: {self.first_name}
Отчество: {self.patronymic}
Компания: {self.company}
Рабочий телефон: {self.work_phone}
Мобильный телефон: {self.mobile_phone}
===================================================
    """
        return result
