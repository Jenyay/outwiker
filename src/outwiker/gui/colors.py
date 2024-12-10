def rgb_to_xyz(rgb):
    r, g, b = rgb
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0

    if r > 0.04045:
        r = ((r + 0.055) / 1.055) ** 2.4
    else:
        r = r / 12.92

    if g > 0.04045:
        g = ((g + 0.055) / 1.055) ** 2.4
    else:
        g = g / 12.92

    if b > 0.04045:
        b = ((b + 0.055) / 1.055) ** 2.4
    else:
        b = b / 12.92

    r = r * 100.0
    g = g * 100.0
    b = b * 100.0

    # Преобразование с использованием матрицы
    x = r * 0.4124 + g * 0.3576 + b * 0.1805
    y = r * 0.2126 + g * 0.7152 + b * 0.0722
    z = r * 0.0193 + g * 0.1192 + b * 0.9505

    return [x, y, z]

def xyz_to_lab(xyz):
    x, y, z = xyz
    x /= 95.047
    y /= 100.000
    z /= 108.883

    if x > 0.008856:
        x = x ** (1/3)
    else:
        x = (7.787 * x) + (16 / 116)

    if y > 0.008856:
        y = y ** (1/3)
    else:
        y = (7.787 * y) + (16 / 116)

    if z > 0.008856:
        z = z ** (1/3)
    else:
        z = (7.787 * z) + (16 / 116)

    l = (116 * y) - 16
    a = 500 * (x - y)
    b = 200 * (y - z)

    return [l, a, b]

def lab_to_xyz(lab):
    l, a, b = lab
    y = (l + 16) / 116
    x = a / 500 + y
    z = y - b / 200

    if y ** 3 > 0.008856:
        y = y ** 3
    else:
        y = (y - 16 / 116) / 7.787

    if x ** 3 > 0.008856:
        x = x ** 3
    else:
        x = (x - 16 / 116) / 7.787

    if z ** 3 > 0.008856:
        z = z ** 3
    else:
        z = (z - 16 / 116) / 7.787

    x *= 95.047
    y *= 100.000
    z *= 108.883

    return [x, y, z]

def xyz_to_rgb(xyz):
    x, y, z = xyz
    x /= 100.0
    y /= 100.0
    z /= 100.0

    r = x * 3.2406 + y * -1.5372 + z * -0.4986
    g = x * -0.9689 + y * 1.8758 + z * 0.0415
    b = x * 0.0557 + y * -0.2040 + z * 1.0570

    if r > 0.0031308:
        r = 1.055 * (r ** (1 / 2.4)) - 0.055
    else:
        r = 12.92 * r

    if g > 0.0031308:
        g = 1.055 * (g ** (1 / 2.4)) - 0.055
    else:
        g = 12.92 * g

    if b > 0.0031308:
        b = 1.055 * (b ** (1 / 2.4)) - 0.055
    else:
        b = 12.92 * b

    r = max(0, min(1, r))
    g = max(0, min(1, g))
    b = max(0, min(1, b))

    return [int(r * 255), int(g * 255), int(b * 255)]

def rgb_to_lab(rgb):
    xyz = rgb_to_xyz(rgb)
    lab = xyz_to_lab(xyz)
    return lab

def lab_to_rgb(lab):
    xyz = lab_to_xyz(lab)
    rgb = xyz_to_rgb(xyz)
    return rgb

if __name__ == "__main__":
    # rgb_color = [0, 0, 0]
    # rgb_color = [255, 255, 255]
    rgb_color = [255, 100, 50]
    lab_color = rgb_to_lab(rgb_color)
    print("RGB to Lab:", lab_color)

    converted_rgb_color = lab_to_rgb(lab_color)
    print("Lab to RGB:", converted_rgb_color)

