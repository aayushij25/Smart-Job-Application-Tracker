# holds config and security

"""
1. create_engine
- Creates a connection interface between your Python application and the database.
- It tells SQLAlchemy which database to connect to.
- It manages communication between Python and the database.
Think of it as establishing a connection between your application and SQLite.

2. sessionmaker
- Creates a factory for generating database sessions.
- A session is used to interact with the database.
- You use sessions to perform operations like inserting, updating, deleting, and retrieving records.
Think of a session as a workspace where you perform database operations.

3. DeclarativeBase
- Provides the base class for defining database models.
- Your database models will inherit from this class.
- SQLAlchemy uses these models to understand the structure of your database tables.
"""

"""
bcrypt is a Python library used for password hashing.
It provides functions to hash passwords and verify them.
"""

"""
Python strings are represented as Unicode text.
However, bcrypt works with bytes rather than Python strings.
.encode() converts a string into bytes (UTF-8 by default).
"""

# A salt is random data added to the password-hashing process to ensure that identical passwords don't necessarily produce identical hashes.

"""
By default, bcrypt.gensalt() uses a work factor of 12.
A higher work factor means more computational effort is required to calculate the hash.
"""

# .decode() converts bytes back into a string (UTF-8 by default).