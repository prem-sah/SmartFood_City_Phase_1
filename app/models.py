from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    email = Column(String(160), unique=True, nullable=False, index=True)
    phone = Column(String(30))
    role = Column(String(30), nullable=False)  # donor, receiver, volunteer, admin
    created_at = Column(DateTime, default=datetime.utcnow)

class Donor(Base):
    __tablename__ = "donors"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_name = Column(String(160), nullable=False)
    organization_type = Column(String(60), nullable=False)
    address = Column(String(250))
    latitude = Column(Float)
    longitude = Column(Float)

class Receiver(Base):
    __tablename__ = "receivers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    organization_name = Column(String(160), nullable=False)
    receiver_type = Column(String(60), nullable=False)
    capacity_meals = Column(Integer, default=0)
    address = Column(String(250))
    latitude = Column(Float)
    longitude = Column(Float)
    verification_status = Column(String(30), default="pending")

class Volunteer(Base):
    __tablename__ = "volunteers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_type = Column(String(60))
    availability = Column(String(30), default="available")
    latitude = Column(Float)
    longitude = Column(Float)

class FoodDonation(Base):
    __tablename__ = "food_donations"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("donors.id"), nullable=False)
    food_name = Column(String(160), nullable=False)
    food_type = Column(String(80), nullable=False)
    quantity_kg = Column(Float, nullable=False)
    estimated_meals = Column(Integer, nullable=False)
    prepared_at = Column(DateTime, nullable=False)
    available_until = Column(DateTime, nullable=False)
    storage_condition = Column(String(120))
    safety_status = Column(String(40), default="pending")
    status = Column(String(40), default="available")
    created_at = Column(DateTime, default=datetime.utcnow)

class FoodAssignment(Base):
    __tablename__ = "food_assignments"

    id = Column(Integer, primary_key=True, index=True)

    donation_id = Column(
        Integer,
        ForeignKey("food_donations.id"),
        nullable=False
    )

    receiver_id = Column(
        Integer,
        ForeignKey("receivers.id"),
        nullable=False
    )

    volunteer_id = Column(
        Integer,
        ForeignKey("volunteers.id"),
        nullable=False
    )

    status = Column(
        String(40),
        default="assigned"
    )

    pickup_time = Column(DateTime, nullable=True)
    delivery_time = Column(DateTime, nullable=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
