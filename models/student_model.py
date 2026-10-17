
from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer, nullable=False)
    course = Column(String(100), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    fee_id = Column(Integer, nullable=True)
    total_fees = Column(Integer, nullable=True)
    paid_fees = Column(Integer, nullable=True)
    pending_fees = Column(Integer, nullable=True)
