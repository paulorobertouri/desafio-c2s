from app.models import Car, CarRq
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Arrange: Setup in-memory SQLite for isolation
test_engine = create_engine('sqlite:///:memory:', echo=False)
TestSession = sessionmaker(bind=test_engine)
Car.metadata.create_all(test_engine)


def make_car(**kwargs):
    defaults = dict(
        brand='Ford', model='Fiesta', year=2018, engine='1.6',
        fuel_type='Gasoline', color='Blue', mileage=30000,
        doors=4, transmission='Manual', price=35000.0,
        description='Compact car.'
    )
    defaults.update(kwargs)
    return Car(**defaults)


def test_get_car_filters_all_fields():
    # Arrange
    rq = CarRq(
        brand='Ford', model='Fiesta', min_year=2015, max_year=2020,
        fuel_type='Gasoline', color='Blue', min_price=20000,
        max_price=40000, transmission='Manual', min_doors=2,
        max_doors=5, min_mileage=10000, max_mileage=50000
    )
    # Act
    filters = Car.get_car_filters(rq)
    # Assert
    assert len(filters) == 13


def test_get_car_filters_partial_fields():
    # Arrange
    rq = CarRq(brand='Ford', min_price=10000)
    # Act
    filters = Car.get_car_filters(rq)
    # Assert
    assert len(filters) == 2


def test_get_car_filters_none():
    # Arrange
    rq = CarRq()
    # Act
    filters = Car.get_car_filters(rq)
    # Assert
    assert filters == []


def test_format_car():
    # Arrange
    car = make_car()
    # Act & Assert
    assert Car.format_car(car) == (
        'Ford Fiesta | 2018 | 1.6 | Gasoline | Blue | 30,000 km | '
        '4 doors | Manual | $35,000.00 | Compact car.'
    )


def test_format_car_no_description():
    # Arrange
    car = make_car(description=None)
    # Act & Assert
    assert Car.format_car(car).endswith(' | ')


def test_format_cars_empty():
    # Act & Assert
    assert Car.format_cars([]) == 'No cars found.'


def test_format_cars_multiple():
    # Arrange
    cars = [make_car(brand='Ford', model='Fiesta'),
            make_car(brand='VW', model='Golf')]
    # Act
    result = Car.format_cars(cars)
    # Assert
    assert result.startswith('Brand Model | Year')
    assert 'Ford Fiesta' in result
    assert 'VW Golf' in result
