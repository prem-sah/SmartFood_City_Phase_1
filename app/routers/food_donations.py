from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodDonation, Donor
from app.schemas import (
    FoodDonationCreate,
    FoodDonationResponse,
    FoodSafetyUpdate
)


router = APIRouter(
    prefix="/food-donations",
    tags=["Food Donations"]
)


@router.post("/", response_model=FoodDonationResponse)
def create_food_donation(
    donation_data: FoodDonationCreate,
    db: Session = Depends(get_db)
):
    donor = (
        db.query(Donor)
        .filter(Donor.id == donation_data.donor_id)
        .first()
    )

    if not donor:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    if donation_data.quantity_kg <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than 0 kg"
        )

    if donation_data.estimated_meals <= 0:
        raise HTTPException(
            status_code=400,
            detail="Estimated meals must be greater than 0"
        )

    if donation_data.available_until <= donation_data.prepared_at:
        raise HTTPException(
            status_code=400,
            detail="Available until time must be after prepared time"
        )

    donation = FoodDonation(
        donor_id=donation_data.donor_id,
        food_name=donation_data.food_name,
        food_type=donation_data.food_type,
        quantity_kg=donation_data.quantity_kg,
        estimated_meals=donation_data.estimated_meals,
        prepared_at=donation_data.prepared_at,
        available_until=donation_data.available_until,
        storage_condition=donation_data.storage_condition,
        safety_status="pending",
        status="available"
    )

    db.add(donation)
    db.commit()
    db.refresh(donation)

    return donation


@router.get("/", response_model=list[FoodDonationResponse])
def get_food_donations(
    db: Session = Depends(get_db)
):
    return db.query(FoodDonation).all()


@router.get("/{donation_id}", response_model=FoodDonationResponse)
def get_food_donation(
    donation_id: int,
    db: Session = Depends(get_db)
):
    donation = (
        db.query(FoodDonation)
        .filter(FoodDonation.id == donation_id)
        .first()
    )

    if not donation:
        raise HTTPException(
            status_code=404,
            detail="Food donation not found"
        )

    return donation
@router.patch("/{donation_id}/safety", response_model=FoodDonationResponse)
def update_food_safety(
    donation_id: int,
    safety_data: FoodSafetyUpdate,
    db: Session = Depends(get_db)
):
    donation = (
        db.query(FoodDonation)
        .filter(FoodDonation.id == donation_id)
        .first()
    )

    if not donation:
        raise HTTPException(
            status_code=404,
            detail="Food donation not found"
        )

    if safety_data.safety_status not in ["approved", "rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Safety status must be approved or rejected"
        )

    donation.safety_status = safety_data.safety_status

    if safety_data.safety_status == "rejected":
        donation.status = "rejected"

    db.commit()
    db.refresh(donation)

    return donation
