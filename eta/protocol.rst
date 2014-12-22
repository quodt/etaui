==================
Tests for protocol
==================

    >>> import sys
    >>> def print_hex(data):
    ...     sys.stdout.write('[')
    ...     sys.stdout.write(', '.join(map(hex, data)))
    ...     sys.stdout.write(']')


reset_seq
=========

    >>> from eta.protocol import reset_seq
    >>> print_hex(reset_seq())
    [0x7b, 0x4d, 0x45, 0x0, 0x0, 0x7d]


init_seq
========

    >>> from eta.protocol import init_seq
    >>> print_hex(init_seq())
    [0x7b, 0x4d, 0x43, 0x19, 0x1d, 0xa, 0x8, 0x0, 0x8, 0x8, 0x0, 0x9, 0x8, 0x0, 0xf, 0x8, 0x0, 0x4b, 0x8, 0x0, 0xc, 0x8, 0x0, 0xb, 0x8, 0x0, 0xa, 0x8, 0x0, 0x46, 0x7d]


get_metric
==========

The method requires a value of list type at least four items. The first two items
defines the metric key, the two latter one defines the value. The byte order
is big-endian.
The return value of the method is tuple with two items in the form (key, value).
Implicitly the returned value get transformed depending on the metric.

All Temperature metrics get dived by 10::

    >>> from eta.protocol import get_metric
    >>> from eta.protocol import NULL, EXHAUST
    >>> get_metric([NULL, EXHAUST, 0x0, 0x0, 0x0])
    (15, 0.0)

    >>> get_metric([NULL, EXHAUST, 0xff, 0xff])
    (15, -0.1)

The metric `CHARGE_CONDITION` is not devided by 10::

    >>> from eta.protocol import CHARGE_CONDITION
    >>> get_metric([NULL, CHARGE_CONDITION, 0x0, 0x7])
    (75, 7)
