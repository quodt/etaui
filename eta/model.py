from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME, FLOAT, INTEGER

Base = declarative_base()


class Entry(Base):

    __tablename__ = 'entries'

    date = Column('date', DATETIME, primary_key=True)
    exhaust = Column('exhaust', FLOAT)
    kettler_flow = Column('kettler_flow', FLOAT)
    kettler_return = Column('kettler_return', FLOAT)
    charge_condition = Column('charge_condition', INTEGER)
    buffer_upper = Column('buffer_upper', FLOAT)
    buffer_middle = Column('buffer_middle', FLOAT)
    buffer_lower = Column('buffer_lower', FLOAT)
    outdoor = Column('outdoor', FLOAT)
