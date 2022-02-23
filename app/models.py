from sqlalchemy import (
    ARRAY,
    JSON,
    TIMESTAMP,
    BigInteger,
    Column,
    Integer,
    SmallInteger,
    String,
    func,
    text,
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Profile(Base):
    __tablename__ = "profile"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    sex = Column(SmallInteger, nullable=False)
    number_of_purchases = Column(Integer, server_default=text("0"))
    avg_price_of_cart = Column(Integer)
    days_since_last_purchase = Column(SmallInteger)
    last_purchase_date = Column(TIMESTAMP(timezone=True))
    average_days_beetween_purchases = Column(SmallInteger)
    average_number_of_purchases = Column(Integer)
    device_list = Column(ARRAY(String(10)))
    locations_list = Column(ARRAY(String(100)))
    last_seen_location = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __mapper_args__ = {"eager_defaults": True}
