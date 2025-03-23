"""
This python module is the database module that will be used to create the database and the User table.
"""

from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from flask_sqlalchemy import SQLAlchemy


class Base(DeclarativeBase):
    """
    This class is to create the Base class.

    Args:
        DeclarativeBase: The base class for the declarative class.
    """
    pass

db = SQLAlchemy(model_class=Base)

class User(db.Model):
    """
    This class is to create the User table.

    Args:
        id (int): The id of the user.
        email (str): The email of the user.
        password (str): The password of the user.
    """
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    
    def __repr__(self):
        """
        Returns the string representation of the User.

        Returns:
            str: The string representation of the User.
        """
        return f"User(id={self.id}, email='{self.email}', password='{self.password}')"
