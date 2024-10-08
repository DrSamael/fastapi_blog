from enum import Enum

class UserRoles(str, Enum):
    user = "user"
    author = "author"
    admin = "admin"
