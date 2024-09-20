from sqlalchemy import Column, Integer, String
from database import Base

class Questions_passenger_satisfaction(Base):
    __tablename__ = "passenger_satisfaction"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(Integer)
    customer_type = Column(String)
    age = Column(Integer)
    travel_type = Column(String)
    trip_class = Column(String)
    flight_distance = Column(Integer)
    inflight_wifi_service = Column(Integer)
    departure_arrival_time_convenient = Column(Integer)
    online_booking = Column(Integer)
    gate_location = Column(Integer)
    food_and_drink = Column(Integer)
    online_boarding = Column(Integer)
    seat_comfort = Column(Integer)
    inflight_entertainment = Column(Integer)
    onboard_service = Column(Integer)
    leg_room_service = Column(Integer)
    baggage_handling = Column(Integer)
    checkin_service = Column(Integer)
    inflight_service = Column(Integer)
    cleanliness = Column(Integer)
    departure_delay_in_minutes = Column(Integer)
    satisfaction = Column(String)
    predicted_satisfaction = Column(String)