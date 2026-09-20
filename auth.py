from fastapi import APIRouter, Depends, HTTPException ,status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..auth import verify_password, create_access_token , hash_password
from ..schemas import User_Response ,UserCreate , UserLogin , TokenResponse 


router = APIRouter(prefix="/auth")

@router.post("/register",response_model=User_Response)
def register(data:UserCreate,db:Session= Depends(get_db)):
    
    hashed_password = hash_password(data.user_password)
    user = User(
    user_name=data.user_name,
    user_email=data.user_email,
    user_address=data.user_address,
    is_address=data.is_address,
    phone_number=data.phone_number,
    user_password = hashed_password
)

    check = db.query(User).filter(User.user_email== data.user_email).first()
    if check  :
         raise HTTPException(
        status_code=400,
        detail="Email already registered"
    )
    
    
    db.add(user)

    
    db.commit()

    db.refresh(user)

    return user


@router.post("/login",response_model=TokenResponse)

def login(data:UserLogin ,db:Session = Depends(get_db)):
     
    user = db.query(User).filter(
    User.user_email == data.user_email
).first()
    if not user:
        raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )

    if not verify_password(data.user_password,user.user_password):
          raise HTTPException(
        status_code=401,
        detail="Invalid email or password"
    )

    token = create_access_token(  
         data={"sub": str(user.user_id)}
)

    return {
    "access_token": token,
    "token_type": "bearer"
}