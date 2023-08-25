import os
from dotenv import load_dotenv
from core.storage import Record
from core.utils import border_msg

load_dotenv()


def paginated_records(phone_book: list) -> str | None:
    """
    Вывод записей из записной книжки постранично. Количество записей на страницу = 10,
    если иное не указано в переменной окружения REC_ON_PAGE в файле .env
    """

    rec_on_page: int = int(os.getenv("REC_ON_PAGE", 10))

    if not phone_book:  # Проверка на наличии записей в телефонная книге
        return print("Телефонная книга пуста.")
    page: int = 1

    # Формирование записей из телефонной книги постранично в читабельном виде
    while phone_book:
        for _ in range(rec_on_page):
            if phone_book:
                record: Record = Record()
                record.__dict__ |= phone_book.pop(0)
                try:
                    print(record.readeble_view())
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
