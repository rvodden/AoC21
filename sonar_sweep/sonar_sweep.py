
def sonar_sweep(depths: list[int]):
    prev = None
    increases = 0
    for current in depths:
        if not prev:
            prev = current
            continue

        increases += 1 if current > prev else 0
        prev = current
    return increases
