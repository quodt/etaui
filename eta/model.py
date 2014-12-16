import time
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.sqlite import DATETIME, FLOAT, INTEGER
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DBSession = scoped_session(sessionmaker())


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

    @staticmethod
    def latest():
        query = DBSession.query(Entry).order_by(Entry.date.desc())
        return query.first()

    def as_dict(self):
        return {
            'date': time.mktime(self.date.timetuple()),
            'exhaust': self.exhaust,
            'kettler_flow': self.kettler_flow,
            'kettler_return': self.kettler_return,
            'charge_condition': self.charge_condition,
            'buffer_upper': self.buffer_upper,
            'buffer_middle': self.buffer_middle,
            'buffer_lower': self.buffer_lower,
            'outdoor': self.outdoor,
        }
