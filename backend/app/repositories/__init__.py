# only place that talks to the database

"""
db.add() - doesn't necessarily execute an INSERT statement immediately.
SQLAlchemy tracks the object and marks it as pending insertion.
The object is now in the session's pending state.

db.commit() - commits the current transaction.
It saves the pending changes permanently to the database.
SQLAlchemy flushes pending changes to the database before committing.
For our new user, it generates an SQL INSERT statement.

db.refresh() - refreshes the Python object using the latest values from the database.
"""