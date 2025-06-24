from sqlalchemy.orm import Session
from app.models import Contact

def find_matching_contacts(db: Session, email: str, phone: str):
    return db.query(Contact).filter(
        (Contact.email == email) | (Contact.phoneNumber == phone)
    ).all()

def create_contact(db: Session, email: str, phone: str, linked_id: int, precedence: str):
    new_contact = Contact(
        email=email,
        phoneNumber=phone,
        linkedId=linked_id,
        linkPrecedence=precedence
    )
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

def get_all_related_contacts(db: Session, primary_id: int):
    return db.query(Contact).filter(
        (Contact.id == primary_id) | (Contact.linkedId == primary_id)
    ).all()
