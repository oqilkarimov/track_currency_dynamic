from typing import TypedDict


class JWTTokenForUser(TypedDict):
    access: str
    refresh: str
