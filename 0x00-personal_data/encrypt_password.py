#!/usr/bin/env python3
"""hash_password"""

from bcrypt import hashpw
from bcrypt import gensalt
from bcrypt import checkpw


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password"""
    password_bytes = password.encode('UTF-8')
    hashed_pwd = hashpw(password_bytes, gensalt())

    return hashed_pwd


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password matches the hashed password"""
    password = password.encode('UTF-8')
    return checkpw(password, hashed_password)
