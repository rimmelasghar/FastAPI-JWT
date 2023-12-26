from passlib.context import CryptContext
from typing import Optional
from sqlalchemy.orm import Session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
