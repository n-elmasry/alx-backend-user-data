#!/usr/bin/env python3
"""BasicAuth class"""
from api.v1.auth.auth import Auth
import base64
from typing import Tuple, TypeVar
from models.user import User


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

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of a Base64 string"""
        if base64_authorization_header is None or not isinstance(
                base64_authorization_header, str):
            return None

        try:
            decoded_header = base64.b64decode(base64_authorization_header)
            return decoded_header.decode('utf-8')
        except (base64.binascii.Error):
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """returns user email and password from the Base64 decoded value"""
        if decoded_base64_authorization_header is None or not isinstance(
                decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        parts = decoded_base64_authorization_header.split(':', 1)

        return (parts[0], parts[1])

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({'email': user_email})
        except Exception:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves the User instance for a request"""
        header = self.authorization_header(request)
        bas64_header = self.extract_base64_authorization_header(header)
        decoded_header = self.decode_base64_authorization_header(
            bas64_header)
        user_cred = self.extract_user_credentials(decoded_header)
        return self.user_object_from_credentials(user_cred[0], user_cred[1])
