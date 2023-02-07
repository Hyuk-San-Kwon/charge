from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, null
#from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    building = Column(Integer,  nullable=False)
    unit = Column(Integer, nullable=False)
    car_number = Column(String, nullable = True)
    elec_car = Column(Integer, nullable = True)
  