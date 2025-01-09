from src.core.domain.entities.base_entity import BaseEntity

from sqlalchemy import Column, String
import bcrypt



class User(BaseEntity):
    __tablename__ = "users"

    name = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False, unique=False)

    @property 
    def password(self):
        raise AttributeError('Password not readable')
    
    @password.setter
    def password(self, password: str) -> None:
        enc_pw = password.encode('utf-8')
        self.password_hash = bcrypt.hashpw(enc_pw, bcrypt.gensalt()).decode('utf-8')
    
    
