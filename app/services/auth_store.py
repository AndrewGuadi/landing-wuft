import os
import sqlite3
from dataclasses import dataclass
from typing import Optional

from flask import Flask
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash


@dataclass
class AuthUser(UserMixin):
    id: int
    email: str
    password_hash: str


def init_auth_db(app: Flask) -> None:
    db_path = _resolve_db_path(app)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def create_user(app: Flask, email: str, password: str) -> AuthUser:
    db_path = _resolve_db_path(app)
    password_hash = generate_password_hash(password)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO users (email, password_hash) VALUES (?, ?)",
                (email.lower(), password_hash),
            )
            user_id = cursor.lastrowid
    except sqlite3.IntegrityError as exc:
        raise ValueError("User already exists.") from exc
    return AuthUser(id=user_id, email=email.lower(), password_hash=password_hash)


def get_user_by_email(app: Flask, email: str) -> Optional[AuthUser]:
    db_path = _resolve_db_path(app)
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT id, email, password_hash FROM users WHERE email = ?",
            (email.lower(),),
        ).fetchone()
    return _row_to_user(row)


def get_user_by_id(app: Flask, user_id: str) -> Optional[AuthUser]:
    db_path = _resolve_db_path(app)
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT id, email, password_hash FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
    return _row_to_user(row)


def authenticate_user(app: Flask, email: str, password: str) -> Optional[AuthUser]:
    user = get_user_by_email(app, email)
    if not user:
        return None
    if not check_password_hash(user.password_hash, password):
        return None
    return user


def _row_to_user(row: Optional[tuple]) -> Optional[AuthUser]:
    if not row:
        return None
    return AuthUser(id=row[0], email=row[1], password_hash=row[2])


def _resolve_db_path(app: Flask) -> str:
    db_path = app.config["AUTH_DB_PATH"]
    if not os.path.isabs(db_path):
        db_path = os.path.abspath(db_path)
    return db_path
