import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.models import BotLink, User, PredictionRecord
from backend.api.auth import get_current_user

router = APIRouter(prefix="/bot", tags=["Telegram Bot API"])

@router.post("/generate-link-code")
def generate_link_code(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    code = secrets.token_hex(4).upper()
    
    # Existing code remove or update
    existing = db.query(BotLink).filter(BotLink.user_id == current_user.id).first()
    if existing:
        existing.link_code = code
        existing.is_active = True
    else:
        new_link = BotLink(
            user_id=current_user.id,
            telegram_chat_id="",
            link_code=code,
            is_active=False
        )
        db.add(new_link)
    db.commit()
    return {"code": code, "instructions": f"Telegram botga /link {code} buyrug'ini yuboring."}

@router.post("/verify-code")
def verify_link_code(code: str, telegram_chat_id: str, db: Session = Depends(get_db)):
    link = db.query(BotLink).filter(BotLink.link_code == code).first()
    if not link:
        raise HTTPException(status_code=404, detail="Yaroqsiz yoki eskirgan ulanish kodi.")
    
    link.telegram_chat_id = telegram_chat_id
    link.is_active = True
    db.commit()

    user = db.query(User).filter(User.id == link.user_id).first()
    return {"status": "success", "username": user.username if user else "Analyst"}
