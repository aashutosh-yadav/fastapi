from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, schemas , utils , oauth2

router = APIRouter(tags=["authentication"])


@router.post("/login")
#def login(user_credientials: schemas.UserLogin, db: Session = Depends(database.get_db)):
def login(user_credientials: OAuth2PasswordRequestForm = Depends() , db: Session = Depends(database.get_db)):

    user = (db.query(models.User).filter(models.User.email == user_credientials.username).first())

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid credientials")


    if not utils.verify(user_credientials.password , user.password): 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail="Invalid credientials")

    

# create and return a token 
    access_token = oauth2.create_access_token(data = {"user_id" : user.id})
    return {"access_token" : access_token , "token_type" : "bearer"}