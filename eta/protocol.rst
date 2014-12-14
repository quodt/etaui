==================
Tests for protocol
==================

    >>> import sys
    >>> def print_hex(data):
    ...     sys.stdout.write('[')
    ...     sys.stdout.write(', '.join(map(hex, data)))
    ...     sys.stdout.write(']')

    >>> from eta.protocol import reset_seq
    >>> print_hex(reset_seq())
    [0x7b, 0x4d, 0x45, 0x0, 0x0, 0x7d]

    >>> from eta.protocol import init_seq
    >>> print_hex(init_seq())
    [0x7b, 0x4d, 0x43, 0x19, 0x1d, 0xa, 0x8, 0x0, 0x8, 0x8, 0x0, 0x9, 0x8, 0x0, 0xf, 0x8, 0x0, 0x4b, 0x8, 0x0, 0xc, 0x8, 0x0, 0xb, 0x8, 0x0, 0xa, 0x8, 0x0, 0x46, 0x7d]