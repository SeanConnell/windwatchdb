def compare_speed(speed, target_speed, tolerance):
    tolerance = abs(tolerance)

    upper_limit = target_speed + tolerance
    lower_limit = target_speed - tolerance

    return lower_limit < speed < upper_limit
