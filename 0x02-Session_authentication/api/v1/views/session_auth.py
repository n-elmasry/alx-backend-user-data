#!/usr/bin/env python3
""" Flask view that handles all routes for the Session authentication."""
from flask import request, make_response
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login() -> str:
    """session"""
    email = request.form.get('email')
    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    password = request.form.get('password')
    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    cookie_name = getenv('SESSION_NAME')

    response = make_response(jsonify(user.to_json()))
    response.set_cookie(cookie_name, session_id)
    return response
