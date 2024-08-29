#!/usr/bin/env python3
""""""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    pattern = '|'.join([f'{field}=.*?(?={separator}|$)' for field in fields])
    return re.sub(
        pattern, lambda m: f'{m.group(0).split("=")[0]}={redaction}', message)
