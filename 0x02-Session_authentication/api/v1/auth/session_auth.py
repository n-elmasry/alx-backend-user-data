#!/usr/bin/env python3
"""SessionAuth"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id.update({str(session_id): user_id})
        return str(session_id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """returns a User ID based on a Session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """(overload) that returns a User instance based on a cookie value"""
        session = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ deletes the user session / logout"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        if self.user_id_for_session_id(session_id) is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
