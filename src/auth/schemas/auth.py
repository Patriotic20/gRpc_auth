from pydantic import BaseModel , Field , field_validator
from core.utils.normalize_string import normalize_string
from auth.utils.password import hash_password



class TokenPayload(BaseModel):
    valid: bool
    user_id: int | None = None
    username: str | None = None
    permissions: list[str] = Field(default_factory=list)



class UserCreate(BaseModel):
    username: str
    password: str
    
    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value : str) -> str:
        return normalize_string(text=value)
    
    
    @field_validator("password", mode="before")
    @classmethod
    def hashed_password(cls, value : str) -> str :
        value = value.strip()
        return hash_password(password=value)
    
    
