from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app import models, schemas, crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/identify", response_model=schemas.IdentifyResponse)
def identify(payload: schemas.IdentifyRequest, db: Session = Depends(get_db)):
    email = payload.email
    phone = payload.phoneNumber

    if not email and not phone:
        raise HTTPException(status_code=400, detail="Email or PhoneNumber required")

    matched_contacts = crud.find_matching_contacts(db, email, phone)

    if not matched_contacts:
        new_contact = crud.create_contact(db, email, phone, None, "primary")
        return {"contact": {
            "primaryContactId": new_contact.id,
            "emails": [new_contact.email] if new_contact.email else [],
            "phoneNumbers": [new_contact.phoneNumber] if new_contact.phoneNumber else [],
            "secondaryContactIds": []
        }}

    primary = min(
        [c for c in matched_contacts if c.linkPrecedence == "primary"],
        key=lambda c: c.createdAt
    )

    for c in matched_contacts:
        if c.linkPrecedence == "primary" and c.id != primary.id:
            c.linkPrecedence = "secondary"
            c.linkedId = primary.id
            db.commit()

    if (email and email not in [c.email for c in matched_contacts if c.email]) or \
       (phone and phone not in [c.phoneNumber for c in matched_contacts if c.phoneNumber]):
        crud.create_contact(db, email, phone, primary.id, "secondary")

    related = crud.get_all_related_contacts(db, primary.id)

    return {"contact": {
        "primaryContactId": primary.id,
        "emails": list({c.email for c in related if c.email}),
        "phoneNumbers": list({c.phoneNumber for c in related if c.phoneNumber}),
        "secondaryContactIds": [c.id for c in related if c.linkPrecedence == "secondary"]
    }}
