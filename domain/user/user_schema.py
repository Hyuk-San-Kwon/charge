from pydantic import BaseModel, validator, EmailStr


class UserCreate(BaseModel):
    building : int
    unit : int
    car_number : str
    elec_car : int
    
class User(BaseModel):
    id: int
    building : int
    unit : int
    car_number : str
    elec_car : int
    
    class Config:
        orm_mode = True