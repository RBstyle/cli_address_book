import os, ast
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
    list_of_records = phone_book.copy()
    if not list_of_records:
        return print("Телефонная книга пуста.")
    page = 1

    while list_of_records:
        for i in range(rec_on_page):
            if list_of_records:
                print(readeble_view(list_of_records.pop(0)))
        if len(list_of_records):
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
