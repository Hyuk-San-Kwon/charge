from sqlalchemy.orm import Session
from domain.user.user_schema import UserCreate
from models import User

def create_user(db: Session, user_create: UserCreate):
    db_user = User(building=user_create.building,
                   unit = user_create.unit,
                   car_number = user_create.car_number,
                   elec_car = user_create.elec_car
                   )
    db.add(db_user)
    db.commit()
    
def get_existing_user(db: Session, user_create: UserCreate):
    return db.query(User).filter(
        (User.car_number == user_create.car_number)
    ).first()
    
def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
