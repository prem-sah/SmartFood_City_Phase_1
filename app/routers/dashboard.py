from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodDonation, Donor
from app.models import (
    Donor,
    Receiver,
    Volunteer,
    FoodDonation,
    FoodAssignment
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def dashboard_summary(db: Session = Depends(get_db)):
    total_donors = db.query(Donor).count()

    total_receivers = db.query(Receiver).count()

    approved_receivers = (
        db.query(Receiver)
        .filter(Receiver.verification_status == "approved")
        .count()
    )

    total_volunteers = db.query(Volunteer).count()

    available_volunteers = (
        db.query(Volunteer)
        .filter(Volunteer.availability == "available")
        .count()
    )

    total_donations = db.query(FoodDonation).count()

    available_donations = (
        db.query(FoodDonation)
        .filter(FoodDonation.status == "available")
        .count()
    )

    approved_donations = (
        db.query(FoodDonation)
        .filter(FoodDonation.safety_status == "approved")
        .count()
    )

    total_assignments = db.query(FoodAssignment).count()

    completed_deliveries = (
        db.query(FoodAssignment)
        .filter(FoodAssignment.status == "completed")
        .count()
    )

    active_deliveries = (
        db.query(FoodAssignment)
        .filter(
            FoodAssignment.status.in_(
                ["assigned", "picked_up", "in_transit"]
            )
        )
        .count()
    )

    total_food_kg = (
        db.query(FoodDonation)
        .with_entities(FoodDonation.quantity_kg)
        .all()
    )

    total_meals = (
        db.query(FoodDonation)
        .with_entities(FoodDonation.estimated_meals)
        .all()
    )

    food_saved_kg = sum(
        row[0] for row in total_food_kg if row[0] is not None
    )

    meals_available = sum(
        row[0] for row in total_meals if row[0] is not None
    )

    return {
        "donors": {
            "total": total_donors
        },
        "receivers": {
            "total": total_receivers,
            "approved": approved_receivers
        },
        "volunteers": {
            "total": total_volunteers,
            "available": available_volunteers
        },
        "food_donations": {
            "total": total_donations,
            "available": available_donations,
            "safety_approved": approved_donations
        },
        "deliveries": {
            "total_assignments": total_assignments,
            "active": active_deliveries,
            "completed": completed_deliveries
        },
        "impact": {
            "food_saved_kg": round(food_saved_kg, 2),
            "meals_available": meals_available
        }
    }


@router.get("/donations")
def dashboard_donations(db: Session = Depends(get_db)):
    donations = (
        db.query(FoodDonation)
        .order_by(FoodDonation.created_at.desc())
        .all()
    )

    result = []

    for donation in donations:
        donor = (
            db.query(Donor)
            .filter(Donor.id == donation.donor_id)
            .first()
        )

        result.append({
            "id": donation.id,
            "food_name": donation.food_name,
            "food_type": donation.food_type,
            "quantity_kg": donation.quantity_kg,
            "estimated_meals": donation.estimated_meals,
            "safety_status": donation.safety_status,
            "status": donation.status,
            "available_until": donation.available_until,
            "donor_name": (
                donor.organization_name
                if donor
                else "Unknown Donor"
            )
        })

    return result


@router.get("/deliveries")
def dashboard_deliveries(db: Session = Depends(get_db)):
    assignments = db.query(FoodAssignment).all()

    return [
        {
            "id": assignment.id,
            "donation_id": assignment.donation_id,
            "receiver_id": assignment.receiver_id,
            "volunteer_id": assignment.volunteer_id,
            "status": assignment.status,
            "pickup_time": assignment.pickup_time,
            "delivery_time": assignment.delivery_time
        }
        for assignment in assignments
    ]


@router.get("/impact")
def dashboard_impact(db: Session = Depends(get_db)):
    donations = db.query(FoodDonation).all()

    total_food_kg = sum(
        donation.quantity_kg
        for donation in donations
        if donation.quantity_kg is not None
    )

    total_meals = sum(
        donation.estimated_meals
        for donation in donations
        if donation.estimated_meals is not None
    )

    completed_deliveries = (
        db.query(FoodAssignment)
        .filter(FoodAssignment.status == "completed")
        .count()
    )

    return {
        "food_saved_kg": round(total_food_kg, 2),
        "meals_distributed": total_meals,
        "completed_deliveries": completed_deliveries
    }
