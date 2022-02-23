from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, NonNegativeInt, PositiveInt, confloat, conint, constr


class Location(BaseModel):
    latitude: confloat(ge=-90, le=90)
    longitude: confloat(ge=-180, le=180)


class ProfileCreate(BaseModel):
    name: constr(strip_whitespace=True, min_length=1, max_length=100)
    sex: conint(ge=0, le=1)
    number_of_purchases: Optional[NonNegativeInt]
    avg_price_of_cart: Optional[NonNegativeInt]
    days_since_last_purchase: Optional[NonNegativeInt]
    last_purchase_date: Optional[datetime]
    average_days_beetween_purchases: Optional[NonNegativeInt]
    average_number_of_purchases: Optional[NonNegativeInt]
    device_list: List[Literal["Mobile", "Web"]]
    locations_list: Optional[List[str]]
    last_seen_location: Optional[Location]


class ProfileUpdate(ProfileCreate):
    name: Optional[constr(strip_whitespace=True, min_length=1, max_length=100)]
    sex: Optional[conint(ge=0, le=1)]
    device_list: Optional[List[Literal["Mobile", "Web"]]]


class Profile(ProfileCreate):
    id: PositiveInt

    class Config:
        orm_mode = True


class ProfileList(BaseModel):
    profiles: List[Profile]
