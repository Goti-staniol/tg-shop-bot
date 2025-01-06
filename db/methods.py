from sqlalchemy.orm import Session, sessionmaker
from .models import (
    User,
    engine
)

def get_session() -> Session:
    Session = sessionmaker(bind=engine)
    return Session()

def get_user(user_id: int, session: Session) -> User:
    return session.query(User).filter(
        User.user_id == user_id
        ).first()

def add_user(user_id: int) -> None:
    try:
        session = get_session()
        new_user = get_user(user_id, session)
        
        if not new_user:
            session.add(User(user_id=user_id))
            session.commit()
    finally:
        session.close()

def update_user_agreement(user_id: int) -> None:
    session = get_session()
    user = get_user(user_id, session)
    
    if user:
        user.agreement_status = True    
        session.commit()
    session.close()

def get_agreement(user_id: int) -> bool:
    session = get_session()
    try:
        user = get_user(user_id, session)
        if user:
            return user.agreement_status
        return False
    finally:
        session.close()

