import time
import serial
from log import log
from protocol import reset_seq, init_seq, read_frame

BAUD = 19200
SERIAL_READ_TIMEOUT = 300
SERIAL_WRITE_TIMEOUT = 5


class Monitor(object):

    def __init__(self, tty):
        self.tty = serial.Serial(tty,
                                 BAUD,
                                 timeout=SERIAL_READ_TIMEOUT,
                                 writeTimeout=SERIAL_WRITE_TIMEOUT)
        self.frame_count = 0
        self.buffer = []
        self.handlers = []
        log.info("Initialized ETA monitor on tty %s", tty)

    def _frame_completed(self):
        data = read_frame(self.buffer)
        if not data:
            log.error("Retreived invalid buffer")
            return
        self._notify(data)

    def _notify(self, data):
        """Call each handler with monitored data
        """
        self.frame_count += 1
        if self.frame_count >= 10:
            self.frame_count = 0
            log.info("Retreived 10 data frames")
        for handler in self.handlers:
            handler(data)

    def _reset(self):
        """Reset ETA from previous initialization
        """
        log.debug("Resetting ETA")
        time.sleep(1)
        try:
            self.tty.write(reset_seq())
            self.tty.flush()
            return True
        except serial.SerialTimeoutException:
            log.error("Unable to reset ETA")
            return False

    def _init(self):
        """Initialize eta to retreive requested metrics
        """
        log.debug("Initializing ETA")
        time.sleep(1)
        try:
            self.tty.write(init_seq())
            self.tty.flush()
            return True
        except serial.SerialTimeoutException:
            log.error("Unable to initialize ETA")
            return False

    def start(self):
        """Init ETA and start monitoring ETA
        """
        if not self._reset():
            return
        if not self._init():
            return
        log.info("Start monitoring ETA...")
        while True:
            try:
                c = self.tty.read(1)
            except serial.SerialTimeoutException:
                log.warn("No data received since %s seconds" %
                         SERIAL_READ_TIMEOUT)
                continue
            if c:
                if c == '{':
                    self.buffer = []
                self.buffer.append(ord(c))
                if c == '}':
                    self._frame_completed()

    def add_handler(self, handler):
        if handler not in self.handlers:
            self.handlers.append(handler)
