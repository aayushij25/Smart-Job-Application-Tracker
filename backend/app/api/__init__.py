# handles HTTP only

"""
Router (FastAPI): Receives the HTTP request.
Schema (Pydantic): Validates the incoming data.
Database (SQLAlchemy): Provides a database session.
Service (Business logic): Registers the user.
Exception handling: Returns an appropriate HTTP error if the email is already registered.
"""

# APIRouter allows us to organize API endpoints into separate groups.

"""
Depends is FastAPI's dependency injection mechanism.
It allows FastAPI to automatically provide something that a function needs.
"""

# HTTPException is used to return an HTTP error response.

# status provides predefined HTTP status codes.

# Decorators modify or register functions.