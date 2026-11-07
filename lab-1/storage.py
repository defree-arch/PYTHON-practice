import sqlite3

DB_FILE = "vault.db"


def _execute(query: str, params: tuple = ()) -> list:
    conn = sqlite3.connect(DB_FILE)
    try:
        rows = conn.execute(query, params).fetchall()
        conn.commit()
        return rows
    finally:
        conn.close()


def init_db() -> None:
    _execute(
        "CREATE TABLE IF NOT EXISTS meta ("
        "key TEXT PRIMARY KEY, value BLOB NOT NULL)"
    )
    _execute(
        "CREATE TABLE IF NOT EXISTS entries ("
        "service TEXT PRIMARY KEY, login TEXT NOT NULL, password BLOB NOT NULL)"
    )


def set_meta(key: str, value: bytes) -> None:
    _execute("INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)", (key, value))


def get_meta(key: str):
    rows = _execute("SELECT value FROM meta WHERE key = ?", (key,))
    return rows[0][0] if rows else None


def add_entry(service: str, login: str, password_encrypted: bytes) -> None:
    _execute(
        "INSERT OR REPLACE INTO entries (service, login, password) VALUES (?, ?, ?)",
        (service, login, password_encrypted),
    )


def get_entry(service: str):
    rows = _execute("SELECT login, password FROM entries WHERE service = ?", (service,))
    return rows[0] if rows else None


def list_services() -> list:
    rows = _execute("SELECT service FROM entries ORDER BY service")
    return [r[0] for r in rows]


def delete_entry(service: str) -> bool:
    if get_entry(service) is None:
        return False
    _execute("DELETE FROM entries WHERE service = ?", (service,))
    return True