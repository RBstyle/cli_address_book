import json
import phonenumbers

from core.phone_book import PhoneBook


def start():
    phone_book = PhoneBook()
    add_record_menu = "1"
    get_all_records_menu = "2"
    edit_record_menu = "3"
    search_record_menu = "4"
    while True:
        print(
            f"""
Добро пожаловать!
Для добавления запись введите: {add_record_menu}
Для просмотра всех записей введите: {get_all_records_menu}
Для редактирование записи введите: {edit_record_menu}
Для поиска ведите: {search_record_menu}
Для выхода ведите: Выход
"""
        )
        menu_answer = input(":")
        if menu_answer == add_record_menu:
            return add_record(phone_book)
        elif menu_answer == get_all_records_menu:
            return get_all_records(phone_book)
        elif menu_answer == edit_record_menu:
            return edit_record(phone_book)
        elif menu_answer == search_record_menu:
            return search_record(phone_book)
        elif menu_answer == "Выход":
            return None
        print("Ввод не корректный!")


def add_record(phone_book: PhoneBook):
    last_name = first_name = patronymic = company = work_phone = mobile_phone = "00"
    while not str_input_validator(last_name):
        print("Введите имя")
        last_name: str = input(":")
    while not str_input_validator(first_name):
        print("Введите Фамилию")
        first_name: str = input(":")
    while not str_input_validator(patronymic):
        print("Введите Отчество")
        patronymic: str = input(":")
    while not 3 < len(company) < 50:
        print("Введите название компании")
        company: str = input(":")
    while not phone_number_validator(work_phone):
        print("Введите номер телефона(раб.)")
        work_phone: str = input(":")
    while not phone_number_validator(mobile_phone):
        print("Введите номер телефона(сот.)")
        mobile_phone: str = input(":")
    record = {
        "last_name": last_name,
        "first_name": first_name,
        "patronymic": patronymic,
        "company": company,
        "work_phone": work_phone,
        "mobile_phone": mobile_phone,
    }
    phone_book.add_record(json.dumps(record))


def get_all_records(phone_book: PhoneBook):
    phone_book.get_all_records()
    return start()


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


def edit_record(phone_book: PhoneBook):
    pass


def search_record(phone_book: PhoneBook):
    pass
