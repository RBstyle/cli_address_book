from typing import NoReturn

from core.phone_book import PhoneBook
from core.utils import border_msg
from core.storage import Record
from core.mesasges import bot_messages


def start() -> NoReturn:
    """Начлало работы с приложением. Все действия и инструкции подробно описаны.
    Управление меню осуществляется через командную строку посредством ввода соответсвтующей цифры пункта меню.
    """

    # при каждом вызове создается новый экземпляр класса с актуальными данными из БД
    phone_book: PhoneBook = PhoneBook()

    while True:
        menu_answer = input(bot_messages.start_menu_message)
        if menu_answer == bot_messages.menu_dict.get("add_record_menu"):
            return add_record(phone_book=phone_book)

        elif menu_answer == bot_messages.menu_dict.get("get_all_records_menu"):
            phone_book.get_all_records()
            return start()

        elif menu_answer == bot_messages.menu_dict.get("get_record_by_id_menu"):
            return get_record(phone_book=phone_book, menu_mode=True)

        elif menu_answer == bot_messages.menu_dict.get("edit_record_menu"):
            return edit_record(phone_book=phone_book)

        elif menu_answer == bot_messages.menu_dict.get("search_record_menu"):
            return search_record(phone_book=phone_book)

        elif menu_answer == "Выход":
            return None
        print("Ввод не корректный!")


def add_record(phone_book: PhoneBook) -> NoReturn:
    """Логика пункта меню добавления записи"""

    record: Record = Record()  # Экземпляр класса Record с дефолтными значениями
    verbose_field_names: dict = record.get_verbose_field_names()
    field_names: dict = record.get_field_names()

    # Генератор сообщений на основе словаря имен полей
    for index in field_names.keys():
        attribute: dict = field_names[index]
        verbose_name: dict = verbose_field_names[index].lower()

        # Запрос информации пока значение не поменяется
        while getattr(record, attribute) == None:
            value: str = input(f"Введите {verbose_name}\n")
            setattr(record, attribute, value)

            # Блок проверки информации. Валидация строковых полей и полей с телефонами
            if record.__annotations__[attribute] is str:
                record.str_validator(attribute, default_data=None)
            if attribute.count("phone"):
                record.phone_validator(attribute, default_data=None)

    # Добавление записи в телефонную книгу(класс PhoneBook)
    result: Record = phone_book.add_record(data=record)

    # Вывод карточки с новой записью и ожидание любого ввода для возврата в меню
    input(result.readeble_view() + "\nНажмите Enter для возврата.")
    return start()


def get_record(phone_book: PhoneBook, menu_mode: bool = False) -> Record | None:
    """Логика пункта меню поиска запиcи по ID"""

    record: dict = dict()

    # Запрос ID пока не будет введен корректный
    while not record:
        input_id: str = input("Введите ID записи\n")

        try:
            record_id: int = int(input_id)
        except:
            border_msg("ID может состоять только из цифр, повторите ввод.")
            continue

        record: Record = phone_book.get_record_by_id(record_id)

    # если функция вызвана не из меню, то возвращаем экземпляр Record
    if not menu_mode:
        return record
    else:
        try:
            result: str = record.readeble_view()
            input(result + "\nНажмите Enter для возврата.")
        except Exception as e:
            border_msg(
                f"Ошибка получения записи: {e}"
            )  # TODO вывести в отдельную функуцию
        return start()


def edit_record(phone_book: PhoneBook):
    """Логика пункта меню редактирования запиcи"""

    record: Record = get_record(phone_book=phone_book)  # Получение записи по ID
    print(
        "Введите новое значение или оставьте поле пустым для сохранения старого значения"
    )
    # Словари имен полей(читабельные и имена в БД)
    verbose_field_names: dict = record.get_verbose_field_names()
    field_names: dict = record.get_field_names()
    currrent_record: dict = record.__dict__.copy()  # Копия текущего состояния записи

    # Генератор сообщений на основе словаря имен полей
    for index in field_names.keys():
        attribute: str = field_names[index]
        verbose_name: str = verbose_field_names[index].lower()
        updated: bool = False

        # Запрос информации пока значение не поменяется
        while not updated:
            current_value = getattr(record, attribute)  # type: str | int
            value: str = input(f"Введите {verbose_name}({current_value})\n")

            if not value:  # Если ответ не вводить сохранится старое значение
                break

            setattr(record, attribute, value)
            print()
            # Блок проверки информации. Валидация строковых полей и полей с телефонами
            if record.__annotations__[attribute] is str:
                if record.str_validator(attribute, default_data=current_value):
                    updated = True

            elif attribute.count("phone"):
                if record.phone_validator(attribute, default_data=current_value):
                    updated = True
            else:  # На случай несанкционированных изменений полей в Record
                border_msg("Неизвестный тип поля! Обратитесь к администратору!")

    # Сохранение изменений в БД
    phone_book.edit_record(new_record=record.__dict__, current_record=currrent_record)
    input(record.readeble_view() + "\nНажмите Enter для возврата.")

    # В объекте PhoneBook изменения не фиксируются, потому что при
    # каждом вызове start() он создается на основе актуальных данных в БД
    return start()


def search_record(phone_book: PhoneBook) -> NoReturn:
    """Логика пункта меню поиска запиcей"""

    # Словари имен полей(читабельные и имена в БД), список возможных критертев
    verbose_field_names: dict = Record().get_verbose_field_names()
    field_names: dict = Record().get_field_names()
    options = verbose_field_names.keys()  # type: dict_keys
    search_terms: list = list()  # Переменная для хранения выбранных критертев

    print("Выберите критерии для поиска:")
    for option, field in verbose_field_names.items():  # Генератор полей для поиска
        print(f"{field} - {option}")

    # Запрос информации пока не получен валидный список критериев для поиска
    while not search_terms:
        input_terms = input(
            f"""
Введите критерии поиска:
(для поиска по нескольким полям введите номера через пробел)
"""
        )
        try:
            list_of_terms = [int(term) for term in input_terms.split()]
            if set(list_of_terms).issubset(options):
                search_terms = list_of_terms
            else:
                raise ValueError()
        except:
            border_msg(
                "Необходимо ввести либо номер ответа либо несколько номеров через пробел!"
            )
    terms_dict: dict = dict()
    for count, _ in verbose_field_names.items():
        if count in search_terms:
            field_name = verbose_field_names[count].lower()
            terms_dict[field_names[count]] = input(f"Введите {field_name}:\n")

    # Запуск поиска по заданным критериям
    phone_book.search_records(search_terms=terms_dict)
    return start()
