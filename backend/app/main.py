from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models import User, Summary

from app.database import Base, engine, get_db
from app.models import User, Summary
from app.schemas import UserCreate, UserResponse, UserLogin, TokenResponse, SummaryCreate, SummaryResponse
from app.auth import hash_password, verify_password, create_access_token, get_current_user
from app.ai_service import generate_summary
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import tempfile

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Client Communication Hub")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-client-communication-hub.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/generate-summary", response_model=SummaryResponse)
def create_summary(
    request: SummaryCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = generate_summary(request.raw_update)

    new_summary = Summary(
        raw_update=request.raw_update,
        summary=result["summary"],
        risks=result["risks"],
        next_steps=result["next_steps"],
        email_draft=result["email_draft"],
        user_id=current_user["user_id"]
    )

    db.add(new_summary)
    db.commit()
    db.refresh(new_summary)

    return new_summary

@app.get("/summaries")
def get_summaries(
    search: str = "",
    page: int = 1,
    limit: int = 5,
    scope: str = "mine",
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(Summary).filter(
        Summary.user_id==current_user["user_id"]
    )

    if search:
        search_term = f"%{search}%"
        query = query.filter(
            Summary.raw_update.ilike(search_term) |
            Summary.summary.ilike(search_term) |
            Summary.risks.ilike(search_term) |
            Summary.next_steps.ilike(search_term) |
            Summary.email_draft.ilike(search_term)
        )

    total = query.count()

    summaries = (
        query
        .order_by(Summary.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "items": summaries,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit
    }

@app.get("/summaries/{summary_id}", response_model=SummaryResponse)
def get_summary(
    summary_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    summary = db.query(Summary).filter(
        Summary.id == summary_id,
        Summary.user_id == current_user["user_id"]
    ).first()

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Summary not found"
        )

    return summary

@app.get("/analytics")
def get_analytics(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_users = db.query(User).count()

    total_summaries = db.query(Summary).count()

    my_summaries = (
        db.query(Summary)
        .filter(Summary.user_id == current_user["user_id"])
        .count()
    )

    return {
        "total_users": total_users,
        "total_summaries": total_summaries,
        "my_summaries": my_summaries,
        "current_user": current_user["email"]
    }

@app.delete("/summaries/{summary_id}")
def delete_summary(
    summary_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    summary = db.query(Summary).filter(
        Summary.id == summary_id,
        Summary.user_id == current_user["user_id"]
    ).first()

    if not summary:
        raise HTTPException(
            status_code=404,
            detail="Summary not found"
        )

    db.delete(summary)
    db.commit()

    return {
        "message": "Summary deleted successfully"
    }

@app.get("/summary/{summary_id}/pdf")
def download_pdf(
    summary_id: int,
    current_user: dict =Depends(get_current_user),
    db: Session = Depends(get_db)
):

    summary = (
        db.query(Summary)
        .filter(
            Summary.id == summary_id,
            Summary.user_id == current_user["user_id"]
        )
        .first()
    )

    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(temp_file.name)

    styles = getSampleStyleSheet()

    content = [
        Paragraph("AI Client Communication Hub", styles["Title"]),
        Spacer(1, 12),

        Paragraph("Summary", styles["Heading2"]),
        Paragraph(summary.summary, styles["BodyText"]),

        Spacer(1, 10),

        Paragraph("Risks", styles["Heading2"]),
        Paragraph(summary.risks, styles["BodyText"]),

        Spacer(1, 10),

        Paragraph("Next Steps", styles["Heading2"]),
        Paragraph(summary.next_steps, styles["BodyText"]),

        Spacer(1, 10),

        Paragraph("Email Draft", styles["Heading2"]),
        Paragraph(summary.email_draft, styles["BodyText"]),
    ]

    doc.build(content)

    return FileResponse(
        temp_file.name,
        media_type="application/pdf",
        filename=f"summary_{summary.id}.pdf"
    )