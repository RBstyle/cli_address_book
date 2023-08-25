class bot_messages:
    """Класс содержит сообщение основного меню приложения и словарь пунктов меню для взаимодействия с объектами приложения.

    Атрибуты
    ----------
    menu_dict : dict
        словарь пунктов меню и соответвующих пунктов навигации {"field_name": index, ...}
    start_menu_message : str
        текст главного меню
    """

    menu_dict: dict = {
        "add_record_menu": "1",
        "get_all_records_menu": "2",
        "get_record_by_id_menu": "3",
        "edit_record_menu": "4",
        "search_record_menu": "5",
    }
    start_menu_message: str = f"""
Добро пожаловать!

Введите "\033[1m{menu_dict.get("add_record_menu")}\033[0m" для добавления записи.
Введите "\033[1m{menu_dict.get("get_all_records_menu")}\033[0m" для просмотра всех записей.
Введите "\033[1m{menu_dict.get("get_record_by_id_menu")}\033[0m" для поиска запиcи по ID.
Введите "\033[1m{menu_dict.get("edit_record_menu")}\033[0m" для редактирования записи.
Введите "\033[1m{menu_dict.get("search_record_menu")}\033[0m" для поиска.
Введите "\033[1mВыход\033[0m" для выхода из приложения.

"""
    verbose_field_names = {
        "last_name": "Имя",
        "first_name": "Фамилия",
        "patronymic": "Отчество",
        "company": "Название компании",
        "work_phone": "Рабочий телефон",
        "mobile_phone": "Мобильный телефон",
    }
