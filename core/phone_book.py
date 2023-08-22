import ast
from pathlib import Path
from typing import Final, NoReturn

from views import paginated_records, readeble_view

BASE_DIR = Path(__file__).resolve().parent.parent
PATH_TO_PHONE_BOOK: Final = f"{BASE_DIR}/data/address_book.txt"


class PhoneBook:
    def __init__(self):
        self.phone_book: list = []
        with open(PATH_TO_PHONE_BOOK, "a+") as phone_book:
            phone_book.seek(0)
            for record in phone_book:
                self.phone_book.append(ast.literal_eval(record))

    def add_record(self, data: str) -> NoReturn:
        with open(PATH_TO_PHONE_BOOK, "a+") as f:
            f.write(data + "\n")
            self.phone_book.append(ast.literal_eval(data))

    def get_all_records(self) -> str:
        return paginated_records(self.phone_book)

    def get_record_by_id(self, id: int) -> str:
        with open(PATH_TO_PHONE_BOOK, "r") as self.phone_book:
            record_by_id = [
                record
                for record in self.phone_book
                if ast.literal_eval(record)["id"] == id
            ]
        if not record_by_id:
            return "Такой записи не существует!"
        return readeble_view(ast.literal_eval(record_by_id[0]))
