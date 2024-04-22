from sqlalchemy import (
    BigInteger,
    Column,
    SmallInteger,
    String,
    Time,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    __table_args__ = {'schema': 'nutritionist'}
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)


class TimeSlot(Base):
    __tablename__ = 'time_slots'
    __table_args__ = {'schema': 'nutritionist'}
    id = Column(BigInteger, primary_key=True, index=True)
    day_of_week = Column(SmallInteger, nullable=False)
    time = Column(Time, nullable=False)
    user_id = Column(
        BigInteger, ForeignKey('nutritionist.users.id'), nullable=False
    )

    user = relationship("User", backref="time_slots")
