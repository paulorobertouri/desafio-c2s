"""
Models and database setup for car search application.
"""

from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from pydantic import BaseModel
from typing import Optional, List
from sqlalchemy.sql.expression import BinaryExpression

Base = declarative_base()

base_dir = os.path.dirname(__file__)
db_dir = os.path.join(base_dir, '..', '.db')
os.makedirs(db_dir, exist_ok=True)
db_path = os.path.join(db_dir, 'cars.db')
engine = create_engine(f'sqlite:///{db_path}', echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class CarRq(BaseModel):
    """
    Pydantic model for car search request filters.
    """

    brand: Optional[str] = None
    model: Optional[str] = None
    min_year: Optional[int] = None
    max_year: Optional[int] = None
    fuel_type: Optional[str] = None
    color: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    transmission: Optional[str] = None
    min_doors: Optional[int] = None
    max_doors: Optional[int] = None
    min_mileage: Optional[int] = None
    max_mileage: Optional[int] = None


class Car(Base):
    """
    SQLAlchemy model for car entity.
    """

    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True, nullable=False)
    model = Column(String, index=True, nullable=False)
    year = Column(Integer, index=True, nullable=False)
    engine = Column(String, nullable=False)
    fuel_type = Column(String, index=True, nullable=False)
    color = Column(String, nullable=False)
    mileage = Column(Integer, nullable=False)
    doors = Column(Integer, nullable=False)
    transmission = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String, nullable=True)

    @classmethod
    def get_car_filters(cls, rq: CarRq) -> List[BinaryExpression]:
        """
        Build SQLAlchemy filter expressions from CarRq.
        """

        filters: List[BinaryExpression] = []
        if rq.brand:
            filters.append(Car.brand.ilike(f"%{rq.brand}%"))
        if rq.model:
            filters.append(Car.model.ilike(f"%{rq.model}%"))
        if rq.min_year is not None:
            filters.append(Car.year >= rq.min_year)
        if rq.max_year is not None:
            filters.append(Car.year <= rq.max_year)
        if rq.fuel_type:
            filters.append(Car.fuel_type.ilike(f"%{rq.fuel_type}%"))
        if rq.color:
            filters.append(Car.color.ilike(f"%{rq.color}%"))
        if rq.min_price is not None:
            filters.append(Car.price >= rq.min_price)
        if rq.max_price is not None:
            filters.append(Car.price <= rq.max_price)
        if rq.transmission:
            filters.append(Car.transmission.ilike(f"%{rq.transmission}%"))
        if rq.min_doors is not None:
            filters.append(Car.doors >= rq.min_doors)
        if rq.max_doors is not None:
            filters.append(Car.doors <= rq.max_doors)
        if rq.min_mileage is not None:
            filters.append(Car.mileage >= rq.min_mileage)
        if rq.max_mileage is not None:
            filters.append(Car.mileage <= rq.max_mileage)
        return filters

    @classmethod
    def format_car(cls, car: 'Car') -> str:
        """
        Format a single car object as a string.
        """

        return (
            f"{car.brand} {car.model} | {car.year} | {car.engine} | "
            f"{car.fuel_type} | {car.color} | {car.mileage:,} km | "
            f"{car.doors} doors | {car.transmission} | "
            f"${car.price:,.2f} | {car.description or ''}"
        )

    @classmethod
    def format_cars(cls, cars: List['Car']) -> str:
        """
        Format a list of car objects as a string table.
        """

        if not cars:
            return "No cars found."
        header = (
            "Brand Model | Year | Engine | Fuel Type | Color | Mileage | "
            "Doors | Transmission | Price | Description"
        )
        cars_list = [cls.format_car(car) for car in cars]
        return header + "\n" + "\n".join(cars_list)
