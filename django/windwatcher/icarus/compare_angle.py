def restrict_angle(angle):
    "make sure any angle falls in the [0..360) range"
    return angle % 360

def compare_angle(a, b, tolerance):
    tolerance=abs(tolerance) # same meaning, easier logic
    difference=min((360) - abs(a - b), abs(a - b))
    return difference <= tolerance

