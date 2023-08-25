import ast, fileinput
from pathlib import Path
from typing import Final, List, NoReturn

from core.paginator import paginated_records
from core.utils import get_last_id, border_msg
from core.storage import Record

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_PHONE_BOOK: Final = f"{BASE_DIR}/data/address_book.txt"


class PhoneBook:
    """
    Класс телефонной книги. При создании экземпляра класса

    в атрибут сохранятеся список актуаллных записей из БД

    Атрибуты
    ----------
    phone_book : List[dict]
        список записей из БД

    Методы
    -------
    add_record(data: Record)
        Добавляет в БД и атрибут phone_book новую запись
    edit_record(data: dict, record: dict)
        Редактирование записи
    get_all_records(self)
        Возвращает все записи из PhoneBook постранично в читабельном виде
    get_record_by_id(id: int)
        Возвращает результат поиска(экземпляр класса Record) записи по ID
    search_records(search_terms: dict)
        Возвращает результат поиска по критериям постранично в читабельном виде
    """

    def __init__(self):
        self.phone_book: List[dict] = list()
        with open(PATH_TO_PHONE_BOOK, "a+") as file:
            file.seek(0)
            for record in file:
                self.phone_book.append(ast.literal_eval(record))

    def add_record(self, data: Record) -> Record:
        """Добавляет в БД и атрибут phone_book новую запись"""

        with open(PATH_TO_PHONE_BOOK, "a+") as f:
            f.write(str(data.__dict__).replace("'", '"') + "\n")
            self.phone_book.append(data.__dict__)
        return self.get_record_by_id(get_last_id())

    def edit_record(self, new_record: dict, current_record: dict):
        """Редактирование записи

        Параметры
        ----------
        new_record : dict
            Словарь с редактированными данными
        current_record : dict
            Словарь с исходными данными для поиска в БД
        """

        current_value: str = str(current_record).replace("'", '"')
        new_value: str = str(new_record).replace("'", '"')

        # Замена исходной записи на новую
        with fileinput.FileInput(
            PATH_TO_PHONE_BOOK, inplace=True, backup=".bak"
        ) as file:
            for line in file:
                print(line.replace(current_value, new_value), end="")

    def get_all_records(self) -> str:
        """Возвращает все записи из PhoneBook постранично в читабельном виде"""

        return paginated_records(self.phone_book)

    def get_record_by_id(self, id: int) -> Record:
        """Возвращает результат поиска(экземпляр класса Record) записи по ID
        Параметры
        ----------
        id: int
            ID записи
        """

        record_by_id = [record for record in self.phone_book if record["id"] == id]

        if not record_by_id:  # Проверка на наличии записи с запрошенным ID
            border_msg("Такой записи не существует!")
            return None

        record: Record = Record()
        record.__dict__ |= record_by_id[0]
        return record

    def search_records(self, search_terms: dict) -> str:
        """Возвращает результат поиска по критериям постранично в читабельном виде
        Параметры
        ----------
        search_terms: dict
            Словарь с критериями поиска и строкой запроса {"field_name": "request", ...}
        """

        search_result: list = list()

        # Поиск записей, удовлетворяющих запросу по критериям
        for field, term in search_terms.items():
            try:
                current_filter: list = [
                    record["id"] for record in self.phone_book if record[field] == term
                ]
            except:
                continue
            if not current_filter:
                continue
            search_result.append(current_filter)

        id_list: set = set(search_result[0])

        # Формирование списка ID записей результата поиска
        for item in search_result[1:]:
            id_list.intersection_update(item)
        result: list = [self.get_record_by_id(id=id).__dict__ for id in list(id_list)]

        if not result:
            return border_msg("Ничего не найдено.")

        return paginated_records(result)
