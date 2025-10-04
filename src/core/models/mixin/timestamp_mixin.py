from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import func

from datetime import datetime


class TimeMixIn:
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), nullable=False)
    
