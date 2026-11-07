import base64
import hashlib
import hmac
import os

from cryptography.fernet import Fernet

SCRYPT_N = 2**14
SCRYPT_R = 8
SCRYPT_P = 1


def new_salt() -> bytes:
    return os.urandom(16)


def _derive(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=32,
    )


def make_hash(password: str, salt: bytes) -> bytes:
    return _derive(password, salt)


def check_password(password: str, salt: bytes, saved_hash: bytes) -> bool:
    return hmac.compare_digest(make_hash(password, salt), saved_hash)


def make_key(password: str, salt: bytes) -> bytes:
    return base64.urlsafe_b64encode(_derive(password, salt))


def encrypt(key: bytes, text: str) -> bytes:
    return Fernet(key).encrypt(text.encode("utf-8"))


def decrypt(key: bytes, data: bytes) -> str:
    return Fernet(key).decrypt(data).decode("utf-8")