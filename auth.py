from passlib.context import CryptContext        #  passilb.context is imported from cryptcontext  used to create verify and hash password 

from jose import JWTError , jwt # JOSE IS USED FOR TOKENS AND JWT IS USED TO ENCODE AND DECODE TOKENES



from datetime import timedelta,timezone,datetime
from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .database import get_db
from .models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated = "auto"
)

SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTE = 30

def hash_password(plain_password : str):
   return  pwd_context.hash(plain_password)

def verify_password( plain_password:str , hashed_password):
   return pwd_context.verify(plain_password,hashed_password)

def create_access_token(data:dict):
   to_encode = data.copy()

   #expire = datetime.now(timedelta.utc) + timedelta(ACCESS_TOKEN_MINUTE)
   expire = datetime.now(timezone.utc) + timedelta(
    minutes=ACCESS_TOKEN_MINUTE
)

   to_encode.update({"exp":expire})

   encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=   ALGORITHM,
   )

   return encoded_jwt


def get_current_user(token:str = Depends(oauth2_scheme),db:Session=Depends(get_db)):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

        token_id = payload.get("sub")
        if token_id is None:
           raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                 detail="Invalid token"
            )
        user = db.query(User).filter(User.user_id == int(token_id)).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
    
        return user

    except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )






       