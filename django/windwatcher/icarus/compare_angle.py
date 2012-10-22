def restrict_angle(angle):
    "make sure any angle falls in the [0..360) range"
    return angle % 360

def compare_angles(a, b, tolerance):
    tolerance=abs(tolerance)
    difference=min((360) - abs(a - b), abs(a - b))
    return difference <= tolerance

