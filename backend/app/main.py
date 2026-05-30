from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, UserLogin, TokenResponse, SummaryCreate
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.ai_service import generate_summary


Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Client Communication Hub")


@app.get("/")
def root():
    return {"message": "AI Client Communication Hub API Running"}


@app.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password_hash=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login", response_model=TokenResponse)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(user.password, existing_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
        data={"sub": existing_user.email, "user_id": existing_user.id}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "email": user.email,
            "password_hash": user.password_hash
        }
        for user in users
    ]

@app.get("/me")
def get_me(current_user: dict = Depends(get_current_user)):
    return current_user

@app.post("/generate-summary")
def create_summary(
    request: SummaryCreate,
    current_user: dict = Depends(get_current_user)
):
    result = generate_summary(request.raw_update)

    return {
        "user": current_user["email"],
        "generated_content": result
    }