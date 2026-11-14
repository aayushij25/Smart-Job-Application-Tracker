# holds business rules

"""
The db: Session part is a type hint.
It tells Python developers and tools that the db parameter is expected to be a SQLAlchemy Session object.
It doesn't create a database connection itself.
The actual session is created elsewhere in your application, usually in your database.py file.
"""