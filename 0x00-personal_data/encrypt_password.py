#!/usr/bin/env python3
"""hash_password"""

import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password matches the hashed password"""
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)
