from app.models import SessionLocal, Car
from sqlalchemy import and_
from sqlalchemy.exc import SQLAlchemyError
from app.parser import parse_car_request
import logging

logging.basicConfig(level=logging.INFO)


def service_search_cars(user_query: str):
    """
    Search cars in the database using provided filters.
    Returns a formatted string with the results or an error message.
    """
    if not user_query or not isinstance(user_query, str):
        return "Invalid query. Please provide a valid search string."
    try:
        with SessionLocal() as session:
            car_rq = parse_car_request(user_query)
            filters = Car.get_car_filters(car_rq)
            query = session.query(Car)
            if filters:
                query = query.filter(and_(*filters))
            query = query.order_by(Car.price.asc())
            results = query.limit(10).all()
            if not results:
                return "No cars found."
            return Car.format_cars(results)
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        return "A database error occurred. Please try again later."
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        return "An unexpected error occurred. Please try again later."
