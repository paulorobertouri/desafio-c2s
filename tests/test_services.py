from unittest.mock import MagicMock
from app.services import service_search_cars
from app.models import Car
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Arrange: Setup in-memory SQLite for isolation
test_engine = create_engine('sqlite:///:memory:', echo=False)
TestSession = sessionmaker(bind=test_engine)
Car.metadata.create_all(test_engine)


def add_car_to_db(**kwargs):
    car = Car(
        brand=kwargs.get('brand', 'Ford'),
        model=kwargs.get('model', 'Fiesta'),
        year=kwargs.get('year', 2018),
        engine=kwargs.get('engine', '1.6'),
        fuel_type=kwargs.get('fuel_type', 'Gasoline'),
        color=kwargs.get('color', 'Blue'),
        mileage=kwargs.get('mileage', 30000),
        doors=kwargs.get('doors', 4),
        transmission=kwargs.get('transmission', 'Manual'),
        price=kwargs.get('price', 35000.0),
        description=kwargs.get('description', 'Compact car.')
    )
    with TestSession() as session:
        session.add(car)
        session.commit()


def test_service_search_cars_success(monkeypatch):
    # Arrange
    add_car_to_db()
    monkeypatch.setattr('app.services.SessionLocal', TestSession)
    mock_parse = MagicMock()
    mock_parse.return_value = type('Rq', (), {
        'brand': 'Ford',
        'model': None,
        'min_year': None,
        'max_year': None,
        'fuel_type': None,
        'color': None,
        'min_price': None,
        'max_price': None,
        'transmission': None,
        'min_doors': None,
        'max_doors': None,
        'min_mileage': None,
        'max_mileage': None
    })()
    monkeypatch.setattr('app.services.parse_car_request', mock_parse)
    # Act
    result = service_search_cars('Ford')
    # Assert
    assert 'Ford Fiesta' in result


def test_service_search_cars_no_results(monkeypatch):
    # Arrange
    monkeypatch.setattr('app.services.SessionLocal', TestSession)
    mock_parse = MagicMock()
    mock_parse.return_value = type('Rq', (), {
        'brand': 'VW', 'model': None,
        'min_year': None, 'max_year': None, 'fuel_type': None, 'color': None,
        'min_price': None, 'max_price': None, 'transmission': None,
        'min_doors': None, 'max_doors': None, 'min_mileage': None,
        'max_mileage': None
    })()
    monkeypatch.setattr('app.services.parse_car_request', mock_parse)
    # Act
    result = service_search_cars('VW')
    # Assert
    assert result == 'No cars found.'


def test_service_search_cars_invalid_query():
    # Act & Assert
    assert service_search_cars(None) == (
        'Invalid query. Please provide a valid search string.'
    )
    assert service_search_cars(123) == (
        'Invalid query. Please provide a valid search string.'
    )


def test_service_search_cars_db_error(monkeypatch):
    # Arrange
    def raise_db(*a, **k):
        raise Exception('fail')
    monkeypatch.setattr('app.services.SessionLocal', raise_db)
    # Act
    result = service_search_cars('Ford')
    # Assert
    assert 'unexpected error' in result.lower()
