from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Receiver
from app.schemas import ReceiverCreate, ReceiverResponse


router = APIRouter(
    prefix="/receivers",
    tags=["Receivers"]
)


@router.post("/", response_model=ReceiverResponse)
def create_receiver(
    receiver_data: ReceiverCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == receiver_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        name=receiver_data.name,
        email=receiver_data.email,
        phone=receiver_data.phone,
        role="receiver"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    receiver = Receiver(
        user_id=user.id,
        organization_name=receiver_data.organization_name,
        receiver_type=receiver_data.receiver_type,
        capacity_meals=receiver_data.capacity_meals,
        address=receiver_data.address,
        latitude=receiver_data.latitude,
        longitude=receiver_data.longitude,
        verification_status="pending"
    )

    db.add(receiver)
    db.commit()
    db.refresh(receiver)

    return receiver


@router.get("/", response_model=list[ReceiverResponse])
def get_receivers(
    db: Session = Depends(get_db)
):
    return db.query(Receiver).all()


@router.get("/{receiver_id}", response_model=ReceiverResponse)
def get_receiver(
    receiver_id: int,
    db: Session = Depends(get_db)
):
    receiver = (
        db.query(Receiver)
        .filter(Receiver.id == receiver_id)
        .first()
    )

    if not receiver:
        raise HTTPException(
            status_code=404,
            detail="Receiver not found"
        )

    return receiver
@router.patch("/{receiver_id}/verify", response_model=ReceiverResponse)
def verify_receiver(
    receiver_id: int,
    db: Session = Depends(get_db)
):
    receiver = (
        db.query(Receiver)
        .filter(Receiver.id == receiver_id)
        .first()
    )

    if not receiver:
        raise HTTPException(
            status_code=404,
            detail="Receiver not found"
        )

    receiver.verification_status = "approved"

    db.commit()
    db.refresh(receiver)

    return receiver
