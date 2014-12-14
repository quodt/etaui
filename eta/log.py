import logging
import sys

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

log = logging.getLogger()

levels = [l for l in logging._levelNames.values() if type(l) is str]


def setup_logging(level=logging.INFO):
    log.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter(FORMAT)
    ch.setFormatter(formatter)
    log.addHandler(ch)
    log.info("Initialized log system")
