def compare_speed(speed, target_speed, tolerance):
    if speed < 0 or target_speed < 0:
        raise ValueError("Speeds may not be negative. Got (%d, %d)" % (speed, target_speed))

    tolerance = abs(tolerance)

    upper_limit = target_speed + tolerance
    lower_limit = target_speed - tolerance

    return lower_limit < speed < upper_limit
