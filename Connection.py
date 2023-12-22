# Defining region codes
INSIDE = 0  # 0000
LEFT = 1  # 0001
RIGHT = 2  # 0010
BOTTOM = 4  # 0100
TOP = 8  # 1000
LEFT_TOP = 9  # 1001
RIGHT_TOP = 10  # 1010
LEFT_BOTTOM = 5  # 0101
RIGHT_BOTTOM = 6  # 0110


def compute_code(area, x, y):
    code = INSIDE

    if x < area[0]:  # to the left of rectangle
        code |= LEFT
    elif x > area[2]:  # to the right of rectangle
        code |= RIGHT

    if y < area[1]:  # below the rectangle
        code |= TOP
    elif y > area[3]:  # above the rectangle
        code |= BOTTOM

    return code


def get_connections(perceptual_hashes, local_areas):
    connections = [{} for _ in range(len(perceptual_hashes) - 1)]

    for i in range(len(local_areas)):
        for j in range(i + 1, len(local_areas)):
            code = compute_code(local_areas[i], local_areas[j][0], local_areas[j][1])
            connections[i][perceptual_hashes[j]] = code

    return connections
