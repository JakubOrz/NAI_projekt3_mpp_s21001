def iloczynskalarny(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Niedopasowane długości wektorów")
    return sum([float(el1) * float(el2) for el1, el2 in zip(v1, v2)])


def normalizuj(v1: list, mocnormalizacji=1):
    dl = sum([float(el) ** 2 for el in v1]) ** 0.5
    v1 = [(float(el) * mocnormalizacji) / dl for el in v1]
    return v1
