from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.params import Body
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/users", tags=["Users"])


# creating user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOUt)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=schemas.UserOUt)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with {id} does not exist",
        )

    return user
