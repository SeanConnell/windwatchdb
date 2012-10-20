def restrict_angle(angle):
    "make sure any angle falls in the [0..360) range"
    return angle % 360

def compare_angle(angle, target_angle, tolerance):
    tolerance= abs(tolerance) # same meaning, easier logic

    angle = restrict_angle(angle)
    upper_limit = restrict_angle(target_angle + tolerance)
    lower_limit = restrict_angle(target_angle - tolerance)

    if upper_limit < lower_limit: # when target_angle close to -180
        upper_limit+= 360

    return (lower_limit <= angle <= upper_limit
        or lower_limit <= angle + 360 <= upper_limit)
