import ast
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
path_to_phone_book = f"{BASE_DIR}/data/address_book.txt"


def get_last_id() -> int:
    """Возвращает ID последней записи, либо 0, если записей нет"""
    with open(path_to_phone_book, "r") as phone_book:
        last_id = [ast.literal_eval(record)["id"] for record in phone_book]

    if last_id:
        return max(last_id)
    return 0


def border_msg(msg: str):
    """Оформляет строку в алерт с границами и красным фоном"""
    row = len(msg)
    h = "".join(["+"] + ["-" * row] + ["+"])
    result = h + "\n" "|" + msg + "|" "\n" + h
    print("\x1b[1;37;41m" + result + "\x1b[0m")
