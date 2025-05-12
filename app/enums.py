from enum import Enum

class RoleEnum(str, Enum):
    ADMIN = "admin"
    PO = "po"
    VIEWER = "viewer"
    EDITOR = "editor"
