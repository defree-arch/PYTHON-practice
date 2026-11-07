
import getpass
import secrets
import string

from cryptography.fernet import InvalidToken

import encryption as crypto
import storage

MAX_ATTEMPTS = 3
MIN_MASTER_LEN = 8


def setup_master() -> bytes:
    print("Первый запуск. Придумайте пароль для входа.")
    while True:
        p1 = getpass.getpass("Пароль для входа: ")
        p2 = getpass.getpass("Повторите пароль: ")
        if len(p1) < MIN_MASTER_LEN:
            print(f"Слишком короткий, минимум {MIN_MASTER_LEN} символов.")
        elif p1 != p2:
            print("Пароли не совпадают.")
        else:
            break
    salt_auth = crypto.new_salt()
    salt_key = crypto.new_salt()
    storage.set_meta("salt_auth", salt_auth)
    storage.set_meta("salt_key", salt_key)
    storage.set_meta("hash", crypto.make_hash(p1, salt_auth))
    return crypto.make_key(p1, salt_key)


def login():
    salt_auth = storage.get_meta("salt_auth")
    salt_key = storage.get_meta("salt_key")
    saved_hash = storage.get_meta("hash")
    for attempt in range(1, MAX_ATTEMPTS + 1):
        password = getpass.getpass("Пароль для входа: ")
        if crypto.check_password(password, salt_auth, saved_hash):
            return crypto.make_key(password, salt_key)
        print(f"Неверный пароль. Осталось попыток: {MAX_ATTEMPTS - attempt}")
    return None


def generate_password(length: int = 16) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*-_"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def show_services() -> None:
    services = storage.list_services()
    if not services:
        print("Записей пока нет.")
        return
    for service in services:
        entry = storage.get_entry(service)
        print(f"  {service}: {entry[0]} / ********")  


def add_account(key: bytes) -> None:
    service = input("Название сервиса: ").strip()
    if not service:
        print("Название не может быть пустым.")
        return
    login_name = input("Логин: ").strip()
    password = getpass.getpass("Пароль (Enter, чтобы сгенерировать): ")
    if not password:
        password = generate_password()
        print(f"Сгенерирован пароль: {password}")
    storage.add_entry(service, login_name, crypto.encrypt(key, password))
    print("Сохранено.")


def get_account(key: bytes) -> None:
    service = input("Название сервиса: ").strip()
    entry = storage.get_entry(service)
    if entry is None:
        print("Такой записи нет.")
        return
    login_name, encrypted = entry
    try:
        print(f"Логин: {login_name}\nПароль: {crypto.decrypt(key, encrypted)}")
    except InvalidToken:
        print("Не удалось расшифровать: данные повреждены.")


def delete_account() -> None:
    service = input("Какой сервис удалить: ").strip()
    if storage.delete_entry(service):
        print("Удалено.")
    else:
        print("Такой записи нет.")


MENU = """
1 - Показать сервисы
2 - Добавить запись
3 - Показать пароль
4 - Удалить запись
5 - Сгенерировать пароль
0 - Выход"""


def menu(key: bytes) -> None:
    while True:
        print(MENU)
        action = input("Выберите действие: ").strip()
        if action == "1":
            show_services()
        elif action == "2":
            add_account(key)
        elif action == "3":
            get_account(key)
        elif action == "4":
            delete_account()
        elif action == "5":
            print(generate_password())
        elif action == "0":
            print("Выход...")
            break
        else:
            print("Нет такого действия.")


def main() -> None:
    storage.init_db()
    if storage.get_meta("hash") is None:
        key = setup_master()
    else:
        key = login()
        if key is None:
            print("Доступ закрыт.")
            return
    menu(key)


if __name__ == "__main__":
    main()