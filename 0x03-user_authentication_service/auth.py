#!/usr/bin/env python3
"""auth"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4
from typing import Union


def _hash_password(password: str) -> bytes:
    """ return salted hash of the input password """
    return hashpw(password.encode('utf-8'), gensalt())


def _generate_uuid() -> str:
    """return a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """hash the password with _hash_password,
        save the user to the database using self._db
        and return the User object."""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError(f'User {email} already exists.')

    def valid_login(self, email: str, password: str) -> bool:
        """check the password If it matches return True. Else return False"""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """Takes email string argument
        Returns the session ID as a string
        Find user corresponding to email, generate new UUID
        store in database as users session_id, return session ID
        """
        new_uuid = _generate_uuid()

        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=new_uuid)
            return str(new_uuid)
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """ takes session_id and returns the corresponding User or None."""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user.email
        except NoResultFound:
            return None
        # return user

    def destroy_session(self, user_id: int) -> None:
        """"updates the corresponding user’s session ID to None."""
        pass
