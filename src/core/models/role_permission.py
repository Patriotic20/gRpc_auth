from .base import Base

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey


class RolePermission(Base):
    
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id", ondelete="CASCADE"))
    