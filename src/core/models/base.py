from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import declared_attr
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import MetaData 

from core.config import settings
from core.utils.case_converter import camel_case_to_snake_case


class Base(DeclarativeBase):
    
    __abstract__ = True 
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    metadata = MetaData(naming_convention=settings.db.naming_convention)
      
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{camel_case_to_snake_case(cls.__name__)}s"
    
    
