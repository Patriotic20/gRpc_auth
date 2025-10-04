from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey , UniqueConstraint

from .base import Base


class UserRole(Base):
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id" , ondelete="CASCADE"))
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id", ondelete="CASCADE"))

    __table_args__ = (UniqueConstraint("user_id", "role_id", name="uq_user_role"),)
    
    
    
