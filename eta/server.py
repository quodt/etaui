import sys
import argparse
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from model import Base, Entry
from log import log, setup_logging, levels
from eta import Monitor
from protocol import (
    EXHAUST,
    KETTLER_FLOW,
    KETTLER_RETURN,
    CHARGE_CONDITION,
    BUFFER_UPPER,
    BUFFER_MIDDLE,
    BUFFER_LOWER,
    OUTDOOR,
)

DBSession = scoped_session(sessionmaker())

# Mapping from ETA Metric identifer to sqlalchemy column
ETA_MODEL_MAP = {
    EXHAUST: Entry.exhaust.key,
    KETTLER_FLOW: Entry.kettler_flow.key,
    KETTLER_RETURN: Entry.kettler_return.key,
    CHARGE_CONDITION: Entry.charge_condition.key,
    BUFFER_UPPER: Entry.buffer_upper.key,
    BUFFER_MIDDLE: Entry.buffer_middle.key,
    BUFFER_LOWER: Entry.buffer_lower.key,
    OUTDOOR: Entry.outdoor.key,
}


def map_data(data):
    """Map given data to sqlalchemy model dict
    """
    mapped = {}
    for k, v in data.items():
        mapped[ETA_MODEL_MAP[k]] = v
    return mapped


def init_db(path='eta.db'):
    """Initialze database
    """
    engine = create_engine("sqlite:///%s" % path)
    Base.metadata.create_all(engine)
    DBSession.configure(bind=engine)
    log.info("Initialized database %s", path)


def create_entry(data):
    """Write data to database
    """
    data = map_data(data)
    entry = Entry(date=datetime.now(), **data)
    DBSession.add(entry)
    DBSession.commit()
    log.debug("Write entry %r", data)


def main(args=None, cb=sys.exit):
    try:
        parser = argparse.ArgumentParser(
            description="Monitoring daemon for ETA",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            )
        parser.add_argument('-d', '--database-path',
                            help="Path to database file",
                            default='var/eta.db')
        parser.add_argument('-t', '--tty',
                            help="TTY of connected ETA",
                            default='/dev/ttyUSB0')
        parser.add_argument('-l', '--level',
                            help="Log level",
                            default='INFO',
                            choices=levels)
        args = parser.parse_args(args)

        setup_logging(args.level)
        init_db(args.database_path)
        monitor = Monitor(args.tty)
        monitor.add_handler(create_entry)
        monitor.start()
    except KeyboardInterrupt:
        log.info("Exiting.")
        return
