#!/usr/bin/env python3
"""BasicAuth class"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """inherits from Auth"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """base64"""
        if authorization_header is None or not isinstance(
                authorization_header, str):
            return None
        if not authorization_header.startswith('Basic '):
            return None
        base64_data = authorization_header[6:]
        return base64_data
