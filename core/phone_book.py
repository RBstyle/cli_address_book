import ast, fileinput

from pathlib import Path
from typing import Final

from core.utils import paginated_records, get_last_id, border_msg
from core.storage import Record

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_PHONE_BOOK: Final = f"{BASE_DIR}/data/address_book.txt"


class PhoneBook:
    def __init__(self):
        self.phone_book: list = []
        with open(PATH_TO_PHONE_BOOK, "a+") as phone_book:
            phone_book.seek(0)
            for record in phone_book:
                self.phone_book.append(ast.literal_eval(record))

    def add_record(self, data: Record):
        with open(PATH_TO_PHONE_BOOK, "a+") as f:
            f.write(data.str_dict() + "\n")
            self.phone_book.append(data.__dict__)
        return self.get_record_by_id(get_last_id())

    def edit_record(self, data: dict, record):
        # self.phone_book.append(data) TODO не обновляет self.phone_book
        record = str(record).replace("'", '"')
        data = str(data).replace("'", '"')
        with fileinput.FileInput(
            PATH_TO_PHONE_BOOK, inplace=True, backup=".bak"
        ) as file:
            for line in file:
                print(line.replace(record, data), end="")

    def get_all_records(self) -> str:
        return paginated_records(self.phone_book)

    def get_record_by_id(self, id: int) -> dict:
        record_by_id = [record for record in self.phone_book if record["id"] == id]
        if not record_by_id:
            print("Такой записи не существует!")
            return {}
        return record_by_id[0]

    def search_records(self, search_terms: dict):
        search_result: list = list()

        for field, term in search_terms.items():
            try:
                current_filter = [
                    record["id"] for record in self.phone_book if record[field] == term
                ]
            except:
                continue

            if not current_filter:
                continue

            search_result.append(current_filter)
        if not search_result:
            return border_msg("Ничего не найдено.")
        id_list = set(search_result[0])
        for s in search_result[1:]:
            id_list.intersection_update(s)

        result = [self.get_record_by_id(id=id) for id in list(id_list)]
        return paginated_records(result)
