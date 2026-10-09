from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import (
    FoodAssignment,
    FoodDonation,
    Receiver,
    Volunteer
)
from app.schemas import (
    FoodAssignmentCreate,
    FoodAssignmentResponse
)


router = APIRouter(
    prefix="/assignments",
    tags=["Food Assignments"]
)


@router.post(
    "/",
    response_model=FoodAssignmentResponse
)
def create_assignment(
    assignment_data: FoodAssignmentCreate,
    db: Session = Depends(get_db)
):
    # Check donation
    donation = (
        db.query(FoodDonation)
        .filter(FoodDonation.id == assignment_data.donation_id)
        .first()
    )

    if not donation:
        raise HTTPException(
            status_code=404,
            detail="Food donation not found"
        )

    # Food must be safety approved
    if donation.safety_status != "approved":
        raise HTTPException(
            status_code=400,
            detail="Food donation must be safety approved"
        )

    # Check receiver
    receiver = (
        db.query(Receiver)
        .filter(Receiver.id == assignment_data.receiver_id)
        .first()
    )

    if not receiver:
        raise HTTPException(
            status_code=404,
            detail="Receiver not found"
        )

    # Receiver must be verified
    if receiver.verification_status != "approved":
        raise HTTPException(
            status_code=400,
            detail="Receiver must be approved before assignment"
        )

    # Check volunteer
    volunteer = (
        db.query(Volunteer)
        .filter(Volunteer.id == assignment_data.volunteer_id)
        .first()
    )

    if not volunteer:
        raise HTTPException(
            status_code=404,
            detail="Volunteer not found"
        )

    # Volunteer must be available
    if volunteer.availability != "available":
        raise HTTPException(
            status_code=400,
            detail="Volunteer is not available"
        )

    # Prevent duplicate assignment
    existing_assignment = (
        db.query(FoodAssignment)
        .filter(
            FoodAssignment.donation_id
            == assignment_data.donation_id
        )
        .first()
    )

    if existing_assignment:
        raise HTTPException(
            status_code=400,
            detail="This food donation is already assigned"
        )

    # Create assignment
    assignment = FoodAssignment(
        donation_id=assignment_data.donation_id,
        receiver_id=assignment_data.receiver_id,
        volunteer_id=assignment_data.volunteer_id,
        status="assigned"
    )

    db.add(assignment)

    # Mark volunteer as busy
    volunteer.availability = "busy"

    db.commit()
    db.refresh(assignment)

    return assignment


@router.get(
    "/",
    response_model=list[FoodAssignmentResponse]
)
def get_assignments(
    db: Session = Depends(get_db)
):
    return db.query(FoodAssignment).all()


@router.get(
    "/{assignment_id}",
    response_model=FoodAssignmentResponse
)
def get_assignment(
    assignment_id: int,
    db: Session = Depends(get_db)
):
    assignment = (
        db.query(FoodAssignment)
        .filter(FoodAssignment.id == assignment_id)
        .first()
    )

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    return assignment


@router.patch(
    "/{assignment_id}/status",
    response_model=FoodAssignmentResponse
)
def update_assignment_status(
    assignment_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    assignment = (
        db.query(FoodAssignment)
        .filter(FoodAssignment.id == assignment_id)
        .first()
    )

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    allowed_statuses = [
        "assigned",
        "picked_up",
        "in_transit",
        "delivered",
        "completed",
        "cancelled"
    ]

    if status not in allowed_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status. Use one of: {allowed_statuses}"
        )

    assignment.status = status

    if status == "picked_up":
        assignment.pickup_time = datetime.utcnow()

    if status in ["delivered", "completed"]:
        assignment.delivery_time = datetime.utcnow()

    # Make volunteer available again after completion/cancellation
    if status in ["completed", "cancelled"]:
        volunteer = (
            db.query(Volunteer)
            .filter(
                Volunteer.id == assignment.volunteer_id
            )
            .first()
        )

        if volunteer:
            volunteer.availability = "available"

    db.commit()
    db.refresh(assignment)

    return assignment
