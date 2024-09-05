#!/usr/bin/env python3
"""a class to manage the API authentication."""
from flask import request
from typing import List, TypeVar
import os


class Auth:
    """to manage the API authentication"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require_auth"""
        if path is None or excluded_paths is None or not excluded_paths:
            return True

        normal_path = path.rstrip('/')

        for excluded_path in excluded_paths:
            normal_excluded_path = excluded_path.rstrip('/')

            if normal_path == normal_excluded_path or normal_path.startswith(
                    normal_excluded_path + '/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """public method """
        if request is None:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """public method """
        return None

    def session_cookie(self, request=None):
        """returns a cookie value from a request"""
        if request is None:
            return None
        return request.cookies.get(os.getenv('SESSION_NAME'))
