import os, ast, phonenumbers
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent
path_to_phone_book = f"{BASE_DIR}/data/address_book.txt"

load_dotenv()


def paginated_records(phone_book: list) -> str:
    """
    Вывод записей из записной книжке постранично. Количество записей на страницу = 10,
    если иное не указано в переменной окружения REC_ON_PAGE в файле .env
    """
    rec_on_page = int(os.getenv("REC_ON_PAGE", 10))
    if not phone_book:
        return print("Телефонная книга пуста.")
    page = 1

    while phone_book:
        for i in range(rec_on_page):
            if phone_book:
                record = phone_book.pop(0)
                try:
                    print(readeble_view(record=record))
                except Exception as e:
                    border_msg(f"Ошибка получения записи: {e}")
        if len(phone_book):
            print(
                f'Страница {page}.\nНажмите ENTER для отображения страницы {page + 1}.(Введите "Старт" для возврата в начало)'
            )
            if input() == "Старт":
                return
        else:
            input(f"Страница {page}.\nНажмите ENTER для выхода из режима просмотра.")
        page += 1
    return


def readeble_view(record: dict) -> str:
    """Приведение записи из телефонной книги в читабельный вид"""
    result = f"""
ID: {record['id']}
Имя: {record['last_name']}
Фамилия: {record['first_name']}
Отчество: {record['patronymic']}
Компания: {record['company']}
Рабочий телефон: {record['work_phone']}
Мобильный телефон: {record['mobile_phone']}
===================================================
"""
    return result


def get_last_id() -> int:
    """Возвращает ID последней записи, либо 0, если записей нет"""
    with open(path_to_phone_book, "r") as phone_book:
        last_id = [ast.literal_eval(record)["id"] for record in phone_book]

    if last_id:
        return max(last_id)
    return 0


def str_input_validator(str: str) -> bool:
    if (
        str.isalpha() and len(str) < 50
    ):  # TODO подумать надо ли проверять на длину ввода
        return True
    else:
        return False


def phone_number_validator(phone_number: str) -> bool:
    # TODO Прикрутить проверку на пустое значение
    number = phonenumbers.parse(phone_number, "RU")
    return phonenumbers.is_valid_number(number)


def border_msg(msg):
    row = len(msg)
    h = "".join(["+"] + ["-" * row] + ["+"])
    result = h + "\n" "|" + msg + "|" "\n" + h
    print("\x1b[1;37;41m" + result + "\x1b[0m")
