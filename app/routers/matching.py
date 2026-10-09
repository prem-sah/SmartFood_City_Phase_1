from math import radians, sin, cos, sqrt, atan2

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import FoodDonation, Donor, Receiver
from app.schemas import ReceiverMatchResponse


router = APIRouter(
    prefix="/matching",
    tags=["Smart Matching"]
)


def calculate_distance(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    """
    Calculate distance between two coordinates
    using the Haversine formula.
    """

    earth_radius_km = 6371.0

    lat1_rad = radians(lat1)
    lat2_rad = radians(lat2)

    delta_lat = radians(lat2 - lat1)
    delta_lon = radians(lon2 - lon1)

    a = (
        sin(delta_lat / 2) ** 2
        + cos(lat1_rad)
        * cos(lat2_rad)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return earth_radius_km * c


@router.get(
    "/donation/{donation_id}",
    response_model=list[ReceiverMatchResponse]
)
def match_receivers(
    donation_id: int,
    db: Session = Depends(get_db)
):
    # -------------------------------------------------
    # 1. Find donation
    # -------------------------------------------------

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

    # -------------------------------------------------
    # 2. Food must be safety approved
    # -------------------------------------------------

    if donation.safety_status != "approved":
        raise HTTPException(
            status_code=400,
            detail="Food donation must be safety approved before matching"
        )

    # -------------------------------------------------
    # 3. Find donor
    # -------------------------------------------------

    donor = (
        db.query(Donor)
        .filter(Donor.id == donation.donor_id)
        .first()
    )

    if not donor:
        raise HTTPException(
            status_code=404,
            detail="Donor not found"
        )

    # -------------------------------------------------
    # 4. Donor location is required
    # -------------------------------------------------

    if donor.latitude is None or donor.longitude is None:
        raise HTTPException(
            status_code=400,
            detail="Donor location is not available"
        )

    donor_latitude = donor.latitude
    donor_longitude = donor.longitude

    # -------------------------------------------------
    # 5. Get only verified/approved receivers
    # -------------------------------------------------

    receivers = (
        db.query(Receiver)
        .filter(
            Receiver.verification_status == "approved"
        )
        .all()
    )

    matches = []

    # -------------------------------------------------
    # 6. Calculate matching score
    # -------------------------------------------------

    for receiver in receivers:

        # Skip receivers without location
        if (
            receiver.latitude is None
            or receiver.longitude is None
        ):
            continue

        # Calculate real distance
        distance = calculate_distance(
            donor_latitude,
            donor_longitude,
            receiver.latitude,
            receiver.longitude
        )

        # ---------------------------------------------
        # Capacity score
        # ---------------------------------------------

        if receiver.capacity_meals >= donation.estimated_meals:

            capacity_score = 100

        elif receiver.capacity_meals > 0:

            capacity_score = (
                receiver.capacity_meals
                / donation.estimated_meals
            ) * 100

        else:

            capacity_score = 0

        # ---------------------------------------------
        # Distance score
        # ---------------------------------------------

        if distance <= 2:
            distance_score = 100

        elif distance <= 5:
            distance_score = 80

        elif distance <= 10:
            distance_score = 60

        elif distance <= 20:
            distance_score = 40

        else:
            distance_score = 20

        # ---------------------------------------------
        # Final weighted score
        # ---------------------------------------------

        match_score = (
            capacity_score * 0.6
            + distance_score * 0.4
        )

        # ---------------------------------------------
        # Recommendation
        # ---------------------------------------------

        if match_score >= 85:

            recommendation = "Highly suitable receiver"

        elif match_score >= 70:

            recommendation = "Suitable receiver"

        elif match_score >= 50:

            recommendation = "Moderately suitable receiver"

        else:

            recommendation = "Low suitability"

        # ---------------------------------------------
        # Add match
        # ---------------------------------------------

        matches.append(
            ReceiverMatchResponse(
                donation_id=donation.id,
                receiver_id=receiver.id,
                receiver_name=receiver.organization_name,
                distance_km=round(distance, 2),
                capacity_meals=receiver.capacity_meals,
                requested_meals=donation.estimated_meals,
                match_score=round(match_score, 2),
                recommendation=recommendation
            )
        )

    # -------------------------------------------------
    # 7. Best receiver first
    # -------------------------------------------------

    matches.sort(
        key=lambda x: x.match_score,
        reverse=True
    )

    return matches