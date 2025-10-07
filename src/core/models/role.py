from sqlalchemy.orm import Mapped , relationship , mapped_column

from .base import Base
from .mixin.timestamp_mixin import TimeMixIn

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .permission import Permission



class Role(Base , TimeMixIn):
    
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary="user_roles", 
        back_populates="roles")
    
    
    permissions: Mapped[list["Permission"]] = relationship(
        "Permission",
        secondary="role_permissions",
        back_populates="roles",
    )
