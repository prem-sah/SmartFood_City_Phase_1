from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Donor
from app.schemas import DonorCreate, DonorResponse

router = APIRouter(
    prefix="/donors",
    tags=["Donors"]
)


@router.post("/", response_model=DonorResponse)
def create_donor(
    donor_data: DonorCreate,
    db: Session = Depends(get_db)
):
    # Check whether email already exists
    existing_user = (
        db.query(User)
        .filter(User.email == donor_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    # Create user
    user = User(
        name=donor_data.name,
        email=donor_data.email,
        phone=donor_data.phone,
        role="donor"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Create donor organization
    donor = Donor(
        user_id=user.id,
        organization_name=donor_data.organization_name,
        organization_type=donor_data.organization_type,
        address=donor_data.address,
        latitude=donor_data.latitude,
        longitude=donor_data.longitude
    )

    db.add(donor)
    db.commit()
    db.refresh(donor)

    return donor


@router.get("/", response_model=list[DonorResponse])
def get_donors(
    db: Session = Depends(get_db)
):
    return db.query(Donor).all()


@router.get("/{donor_id}", response_model=DonorResponse)
def get_donor(
    donor_id: int,
    db: Session = Depends(get_db)
):
    donor = (
        db.query(Donor)
        .filter(Donor.id == donor_id)
        .first()
    )

    if not donor:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    return donor
