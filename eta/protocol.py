import struct

START_1 =          0x7B  # {
START_2 =          0x4D  # M
END =              0x7D  # }

NULL =             0x00
SH10 =             0x08

RESET =            0x45
INIT =             0x43

EXHAUST =          0x0F
KETTLER_FLOW =     0x08
KETTLER_RETURN =   0x09
CHARGE_CONDITION = 0x4B
BUFFER_UPPER =     0x0C
BUFFER_MIDDLE =    0x0B
BUFFER_LOWER =     0x0A
OUTDOOR =          0x46

DATA_INTERVAL =    0x0A   # 10 seconds

reset = [0x7B, 0x4D, 0x45, 0x00, 0x00, 0x7D]
init = [0x7B, 0x4D, 0x43,         # {MC
        0x19,                     # length
        0x1D,                     # checksumme
        0x0a,                     # interval
        0x08, 0x00, 0x08,         # Kessel Vorlauftempleratur
        0x08, 0x00, 0x09,         # Kessel Ruecklauftemperatur
        0x08, 0x00, 0x0f,         # Abgastemperatur
        0x08, 0x00, 0x4b,         # Puffer Ladezustand
        0x08, 0x00, 0x0c,         # Puffer Temperatur oben
        0x08, 0x00, 0x0b,         # Puffer Temperatur mitte
        0x08, 0x00, 0x0a,         # Puffer Temperatur unten
        0x08, 0x00, 0x46,         # Aussentemperatur
        0x7D]                     # }

DATA_OFFSET      = 5
INDEX_OFFSET     = 1
RESP_PACKAGE_LEN = 5


# writing part
#
def seq(cmd, metrics=[]):
    bytes = []
    bytes.append(START_1)
    bytes.append(START_2)
    bytes.append(cmd)
    bytes.append(len(metrics) * 3 + bool(metrics))
    cs = (sum(metrics)
          + len(metrics) * SH10
          + bool(metrics) * DATA_INTERVAL) % 255
    bytes.append(cs)
    if metrics:
        bytes.append(DATA_INTERVAL)
    for m in metrics:
        bytes.append(SH10)
        bytes.append(NULL)
        bytes.append(m)
    bytes.append(END)
    return bytes


def reset_seq():
    return seq(RESET)


def init_seq():
    return seq(INIT, [
        KETTLER_FLOW,
        KETTLER_RETURN,
        EXHAUST,
        CHARGE_CONDITION,
        BUFFER_UPPER,
        BUFFER_MIDDLE,
        BUFFER_LOWER,
        OUTDOOR
    ])


# Reading part
#
def div_by_ten(v):
    return float(v) / 10


metric_modifier = {
    EXHAUST:          div_by_ten,
    KETTLER_FLOW:     div_by_ten,
    KETTLER_RETURN:   div_by_ten,
    BUFFER_UPPER:     div_by_ten,
    BUFFER_MIDDLE:    div_by_ten,
    BUFFER_LOWER:     div_by_ten,
    OUTDOOR:          div_by_ten,
    CHARGE_CONDITION: lambda x: x,
}


def get_metric(data):
    """Read key-value pair from raw data fragment
    """
    key, raw = struct.unpack('>hh', ''.join(map(chr, data)))
    return key, metric_modifier[key](raw)


def read_frame(frame):
    """Read data from frame
    """
    if len(frame) != 46:
        return None
    raw = frame[DATA_OFFSET + INDEX_OFFSET:]
    data = {}
    for i in range(0, len(raw), RESP_PACKAGE_LEN):
        k, v = get_metric(raw[i:i + RESP_PACKAGE_LEN])
        data[k] = v
    return data
