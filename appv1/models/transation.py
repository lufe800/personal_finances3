from sqlalchemy import Column,Integer, ForeignKey, CHAR, SMALLINT, Float, Enum, Date
from appv1.models.base_class import Base
from sqlalchemy.orm import relationship
import enum

class TransationType(enum.Enum):
    revenue = "revenue"
    expenses = "expenses"
    
class Transation(Base):
    __tablename__ = 'transantion'
    transation_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(CHAR(30), ForeignKey('user.user_id'))
    category_id = Column(SMALLINT(3), ForeignKey('category.category_id'))
    amout = Column(Float(10,2))
    t_type = Column(Enum(TransationType))
    t_date = Column(Date) 
    
    user = relationship("User")
    category = relationship("Category")