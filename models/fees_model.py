
from sqlalchemy import Column, Integer, ForeignKey, Boolean
from database import Base


class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    total_fees = Column(Integer, nullable=False)
    paid_fees = Column(Integer, default=0, nullable=False)
    pending_fees = Column(Integer, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
