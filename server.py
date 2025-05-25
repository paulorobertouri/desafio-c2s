"""
Server module for car search application.
Handles incoming requests and queries the database for matching cars.
"""
from app.services import service_search_cars
from mcp.server.fastmcp import FastMCP
import logging

logging.basicConfig(level=logging.INFO)
mcp = FastMCP("Server")


@mcp.tool("search_cars")
def search_cars(user_query: str):
    """
    Search cars in the database using provided filters.
    Returns a formatted string with the results or an error message.
    """
    return service_search_cars(user_query)


if __name__ == "__main__":
    mcp.run()
