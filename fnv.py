def fnv32a (_string):
    _string = _string[:50]
    hval = 0x811c9dc5
    fnv_32_prime = 0x01000193
    uint32_max = 2 ** 32
    for s in _string:
        hval = hval ^ ord(s)
        hval = (hval * fnv_32_prime) % uint32_max
    return str(hval)