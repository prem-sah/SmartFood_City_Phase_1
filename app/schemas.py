from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class DonorCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

    organization_name: str
    organization_type: str

    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class DonorResponse(BaseModel):
    id: int
    user_id: int

    organization_name: str
    organization_type: str

    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True


class ReceiverCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

    organization_name: str
    receiver_type: str

    capacity_meals: int = 0

    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class ReceiverResponse(BaseModel):
    id: int
    user_id: int

    organization_name: str
    receiver_type: str

    capacity_meals: int

    address: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    verification_status: str

    class Config:
        from_attributes = True


class FoodDonationCreate(BaseModel):
    donor_id: int

    food_name: str
    food_type: str

    quantity_kg: float
    estimated_meals: int

    prepared_at: datetime
    available_until: datetime

    storage_condition: Optional[str] = None


class FoodDonationResponse(BaseModel):
    id: int
    donor_id: int

    food_name: str
    food_type: str

    quantity_kg: float
    estimated_meals: int

    prepared_at: datetime
    available_until: datetime

    storage_condition: Optional[str] = None

    safety_status: str
    status: str

    class Config:
        from_attributes = True

class FoodSafetyUpdate(BaseModel):
    safety_status: str
class ReceiverMatchResponse(BaseModel):
    donation_id: int
    receiver_id: int
    receiver_name: str
    distance_km: float
    capacity_meals: int
    requested_meals: int
    match_score: float
    recommendation: str
class VolunteerCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

    vehicle_type: Optional[str] = None
    availability: str = "available"

    latitude: Optional[float] = None
    longitude: Optional[float] = None


class VolunteerResponse(BaseModel):
    id: int
    user_id: int

    vehicle_type: Optional[str] = None
    availability: str

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    class Config:
        from_attributes = True

class FoodAssignmentCreate(BaseModel):
    donation_id: int
    receiver_id: int
    volunteer_id: int


class FoodAssignmentResponse(BaseModel):
    id: int

    donation_id: int
    receiver_id: int
    volunteer_id: int

    status: str

    pickup_time: Optional[datetime] = None
    delivery_time: Optional[datetime] = None

    created_at: datetime

    class Config:
        from_attributes = True
