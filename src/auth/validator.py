from src.auth.models import User
from typing import Optional
from sqlalchemy.orm import Session


async def verify_email_exist(email: str, db_session: Session) -> Optional[User]:
    return db_session.query(User).filter(User.email == email).first()