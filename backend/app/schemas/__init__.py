# defines the request and response shapes

"""
Pydantic is a Python library used for:
- Validating incoming data.
- Checking data types.
- Converting data into the expected types when possible.
- Defining the structure of data.
"""

# Field() allows you to add additional validation rules and metadata to a field.

"""
SQLAlchemy model: (How is data stored?)
Defines database structure	
Maps Python objects to database tables	
Handles database columns	
Mapped[int]	

Pydantic schema: (What data can enter or leave the API?)
Defines API data structure
Validates incoming/outgoing data
Handles request/response fields
id: int
"""