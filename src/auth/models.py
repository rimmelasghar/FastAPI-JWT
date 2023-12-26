from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.db.database import Base
from src.auth import utils

class User(Base):
    __tablename__ = "user"

    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(50))
    email = Column(String(255),unique=True)
    role = Column(String(50),nullable=True,default="user")
    firstName = Column(String(50))
    lastName = Column(String(50))
    password = Column(String(255))

    # blogs = relationship("Blog", back_populates="author", primaryjoin="User.id == Blog.author_id")


    def __init__(self, username, email, role, password, firstName, lastName, *args, **kwargs):
        self.username = username
        self.email = email
        self.role = role
        self.firstName = firstName
        self.lastName = lastName
        self.password = utils.get_password_hash(password)

    def check_password(self, password):
        return utils.verify_password(self.password, password)
    
    class Config:
        orm_mode = True