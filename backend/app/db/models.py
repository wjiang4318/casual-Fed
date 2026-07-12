from sqlalchemy import Column, Integer, String, Float, DateTime, Date, JSON
from sqlalchemy.orm import DeclarativeBase


# we are constructing an ORM layer, fully pythonic mapping classes to tables. 
'''
Relational databases think in tables, rows, columns
Python thinks in objects, classes, attributes
ORM maps them together so a class = table, an instance = row, and an attribute = column
Python Class          Database Table
─────────────         ──────────────
class User     →      table: users
  id           →        column: id (INTEGER)
  name         →        column: name (VARCHAR)
  age          →        column: age (INTEGER)

user = User()  →      a single row in that table
'''

# Base inherits from DeclarativeBase, giving SQLAlchemy the ability to track 
# all models that inherit from Base. pass = nothing extra to add.

class Base(DeclarativeBase):
    pass

# Our class meeting inherits from Base. So meeting automatically gets all the hidden SQLAlchemy machinery that Base pulled in from DeclarativeBase
class Meeting(Base):
    __tablename__ = "meetings"
    id = Column(Integer, primary_key=True) # each column(...) defines a column in the table, specifying the python attribute name, data type, and optional constraints
    date = Column(Date, unique=True) # date will be known when parsing and converted to datetime via python
    decision = Column(String)
    magnitude_bps = Column(Integer)
    tone = Column(String)
    tone_confidence = Column(Float)
    statement_text = Column(String)
    created_at = Column(DateTime)
    statement_diff_json = Column(JSON)