from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship


from typing import TYPE_CHECKING

from core.models.mixin.timestamp_mixin import TimeMixIn
from .base import Base


if TYPE_CHECKING:
    from .role import Role

class Permission(Base, TimeMixIn):
    
    name: Mapped[str] = mapped_column(unique=True, nullable=False)
    
    roles: Mapped[list["Role"]] = relationship(
        "Role",
        secondary="role_permissions",
        back_populates="permissions",
    )
    
    
