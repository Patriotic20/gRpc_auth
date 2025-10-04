from sqlalchemy.orm import Mapped, mapped_column 
from sqlalchemy.orm import relationship

from typing import TYPE_CHECKING
from core.models.mixin.timestamp_mixin import TimeMixIn


from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .permission import Permission


class Role(Base, TimeMixIn):
    
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
