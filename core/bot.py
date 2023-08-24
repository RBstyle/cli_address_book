from core.phone_book import PhoneBook
from core.storage import Record
from core.utils import (
    str_input_validator,
    phone_number_validator,
    readeble_view,
    border_msg,
)


def start():
    """Starts the bot"""
    phone_book = PhoneBook()
    add_record_menu = "1"
    get_all_records_menu = "2"
    get_record_by_id_menu = "3"
    edit_record_menu = "4"
    search_record_menu = "5"
    while True:
        print(
            f"""
Добро пожаловать!

Для добавления запись введите: {add_record_menu}
Для просмотра всех записей введите: {get_all_records_menu}
Для поиска запиcи по ID введите: {get_record_by_id_menu}
Для редактирование записи введите: {edit_record_menu}
Для поиска ведите: {search_record_menu}
Для выхода ведите: Выход
"""
        )
        menu_answer = input(":")
        if menu_answer == add_record_menu:
            return add_record(phone_book=phone_book)

        elif menu_answer == get_all_records_menu:
            return get_all_records(phone_book=phone_book)

        elif menu_answer == get_record_by_id_menu:
            record = get_record(phone_book=phone_book)

            try:
                result = readeble_view(record=record)
                input(result + "\nНажмите Enter для возврата.")
            except Exception as e:
                border_msg(
                    f"Ошибка получения записи: {e}"
                )  # TODO вывести в отдельную функуцию
            return start()

        elif menu_answer == edit_record_menu:
            return edit_record(phone_book=phone_book)

        elif menu_answer == search_record_menu:
            return search_record(phone_book=phone_book)

        elif menu_answer == "Выход":
            return None
        print("Ввод не корректный!")


def add_record(phone_book: PhoneBook):
    """Entering information to create an record"""
    last_name = first_name = patronymic = company = work_phone = mobile_phone = "00"
    while not str_input_validator(last_name):
        print("Введите имя")
        last_name: str = input(":")
    while not str_input_validator(first_name):
        print("Введите фамилию")
        first_name: str = input(":")
    while not str_input_validator(patronymic):
        print("Введите отчество")
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
    data = Record(
        last_name=last_name,
        first_name=first_name,
        patronymic=patronymic,
        company=company,
        work_phone=work_phone,
        mobile_phone=mobile_phone,
    )
    result = phone_book.add_record(data=data)
    input(readeble_view(result) + "\nНажмите Enter для возврата.")
    return start()


def get_all_records(phone_book: PhoneBook):
    phone_book.get_all_records()
    return start()


def get_record(phone_book: PhoneBook):
    print("Введите ID записи")
    record = {}
    while not record:
        input_id = input(":")

        try:
            record_id = int(input_id)
        except:
            border_msg("ID может состоять только из цифр, повторите ввод.")
            continue

        record = phone_book.get_record_by_id(int(record_id))
    return record


def edit_record(phone_book: PhoneBook):
    last_name = first_name = patronymic = company = work_phone = mobile_phone = "00"
    record = get_record(phone_book=phone_book)
    record_id = record["id"]
    print(
        "Введите новое значение или оставьте поле пустым для сохранения старого значения"
    )

    while not str_input_validator(last_name):
        last_name = input(f"Имя({record['last_name']}): ")
        if not last_name:
            last_name = record["last_name"]

    while not str_input_validator(first_name):
        first_name = input(f"Фамилия({record['first_name']}): ")
        if not first_name:
            first_name = record["first_name"]

    while not str_input_validator(patronymic):
        patronymic = input(f"Отчество({record['patronymic']}): ")
        if not patronymic:
            patronymic = record["patronymic"]

    while not str_input_validator(company):
        company = input(f"Название компании({record['company']}): ")
        if not company:
            company = record["company"]

    while not phone_number_validator(work_phone):
        work_phone = input(f"Рабочий телефон({record['work_phone']}): ")
        if not work_phone:
            work_phone = record["work_phone"]

    while not phone_number_validator(mobile_phone):
        mobile_phone = input(f"Мобильный телефон({record['mobile_phone']}): ")
        if not mobile_phone:
            mobile_phone = record["mobile_phone"]
    data = {
        "id": int(record_id),
        "last_name": last_name,
        "first_name": first_name,
        "patronymic": patronymic,
        "company": company,
        "work_phone": work_phone,
        "mobile_phone": mobile_phone,
    }
    phone_book.edit_record(data, record)
    record = phone_book.get_record_by_id(int(record_id))
    input(readeble_view(data) + "\nНажмите Enter для возврата.")
    return start()


def search_record(phone_book: PhoneBook):
    verbose_fields = Record().get_verbose_field_names()
    fields = Record().get_field_names()
    options = verbose_fields.keys()
    search_terms: list = list()
    print("Выберите критерий для поиска:")
    for count, key in verbose_fields.items():
        print(f"{key} - {count}")
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
    for count, _ in verbose_fields.items():
        if count in search_terms:
            field_name = verbose_fields[count].lower()
            terms_dict[fields[count]] = input(f"Введите {field_name}:\n")
    phone_book.search_records(search_terms=terms_dict)
    return start()
