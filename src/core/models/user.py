from sqlalchemy.orm import Mapped , relationship

from .mixin.timestamp_mixin import TimeMixIn
from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .role import Role


class User(Base , TimeMixIn):
    
    username: Mapped[str]
    password: Mapped[str]
    
    
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="user_roles",
        back_populates="users"
    )
