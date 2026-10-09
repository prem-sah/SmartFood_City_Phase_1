from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Volunteer
from app.schemas import VolunteerCreate, VolunteerResponse


router = APIRouter(
    prefix="/volunteers",
    tags=["Volunteers"]
)


@router.post("/", response_model=VolunteerResponse)
def create_volunteer(
    volunteer_data: VolunteerCreate,
    db: Session = Depends(get_db)
):
    # Check if email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == volunteer_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create user
    user = User(
        name=volunteer_data.name,
        email=volunteer_data.email,
        phone=volunteer_data.phone,
        role="volunteer"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create volunteer profile
    volunteer = Volunteer(
        user_id=user.id,
        vehicle_type=volunteer_data.vehicle_type,
        availability=volunteer_data.availability,
        latitude=volunteer_data.latitude,
        longitude=volunteer_data.longitude
    )

    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)

    return volunteer


@router.get("/", response_model=list[VolunteerResponse])
def get_volunteers(
    db: Session = Depends(get_db)
):
    return db.query(Volunteer).all()


@router.get("/{volunteer_id}", response_model=VolunteerResponse)
def get_volunteer(
    volunteer_id: int,
    db: Session = Depends(get_db)
):
    volunteer = (
        db.query(Volunteer)
        .filter(Volunteer.id == volunteer_id)
        .first()
    )

    if not volunteer:
        raise HTTPException(
            status_code=404,
            detail="Volunteer not found"
        )

    return volunteer
