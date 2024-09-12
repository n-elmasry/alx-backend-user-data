#!/usr/bin/env python3
"""auth"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> bytes:
    """ return salted hash of the input password """
    return hashpw(password.encode('utf-8'), gensalt())
