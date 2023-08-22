def main():
    add_record_menu = "Добавить"
    get_records_menu = "Просмотр"
    print(
        f"""
Добро пожаловать!
Для добавления запсис введите: {add_record_menu}
Для просмотра записей введите: {get_records_menu}
"""
    )
    menu_answer = input(":")
    if menu_answer == add_record_menu:
        pass


if __name__ == "__main__":
    main()
