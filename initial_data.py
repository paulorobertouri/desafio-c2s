"""
Script to populate the database with initial fake car data for testing.
"""

import os
from faker import Faker
import random
from app.models import Base, Car, engine, SessionLocal
import logging

logging.basicConfig(level=logging.INFO)

db_directory = os.path.join(os.path.dirname(__file__), '.db')
os.makedirs(db_directory, exist_ok=True)
Base.metadata.create_all(bind=engine)

brands_models = {
    'Toyota': ['Corolla', 'Camry', 'Yaris', 'Hilux'],
    'Ford': ['Fiesta', 'Focus', 'Ranger', 'Fusion'],
    'Honda': ['Civic', 'Fit', 'HR-V', 'City'],
    'Chevrolet': ['Onix', 'Prisma', 'Cruze', 'S10'],
    'Volkswagen': ['Golf', 'Polo', 'Tiguan', 'Jetta'],
    'Hyundai': ['HB20', 'Creta', 'Tucson', 'Elantra'],
}
fuel_types = ['Gasoline', 'Ethanol', 'Diesel', 'Flex', 'Hybrid', 'Electric']
colors = ['Black', 'White', 'Silver', 'Red', 'Blue', 'Gray', 'Green']
transmissions = ['Manual', 'Automatic', 'CVT']
engines = ['1.0', '1.2', '1.4', '1.6', '2.0', '2.2 Turbo', 'Electric']


def random_car(fake: Faker) -> Car:
    """
    Generate a random Car instance using Faker.
    """
    brand = random.choice(list(brands_models.keys()))
    model = random.choice(brands_models[brand])
    year = random.randint(2005, 2024)
    engine = random.choice(engines)
    fuel_type = random.choice(fuel_types)
    color = random.choice(colors)
    mileage = random.randint(0, 250_000)
    doors = random.choice([2, 4])
    transmission = random.choice(transmissions)
    price = round(random.uniform(5000, 200000), 2)
    description = fake.sentence(nb_words=10)
    return Car(
        brand=brand,
        model=model,
        year=year,
        engine=engine,
        fuel_type=fuel_type,
        color=color,
        mileage=mileage,
        doors=doors,
        transmission=transmission,
        price=price,
        description=description
    )


def main():
    """
    Populate the database with fake car data.
    """
    fake = Faker()
    try:
        with SessionLocal() as session:
            # Clear existing data
            session.query(Car).delete()
            # Generate and add new car data
            cars = [random_car(fake) for _ in range(100)]
            session.add_all(cars)
            session.commit()
            logging.info('Database populated with 100 fake cars.')
    except Exception as e:
        logging.error(f"Error populating database: {e}")
        raise


if __name__ == '__main__':
    main()
