import numpy as np


def rgb_to_hsl(pixels):
    hue_data = []
    saturation_data = []
    lightness_data = []

    r_chanel, g_chanel, b_chanel = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]

    for line in range(len(pixels)):
        hue_line = []
        saturation_line = []
        lightness_line = []

        for col in range(len(pixels[line])):
            r, g, b = r_chanel[line][col] / 255, g_chanel[line][col] / 255, b_chanel[line][col] / 255

            c_max = max(r, g, b)
            c_min = min(r, g, b)
            delta = c_max - c_min

            lightness = (c_max + c_min) / 2

            if delta == 0:
                hue = saturation = 0
            else:
                saturation = delta / (1 - abs(2 * lightness - 1))
                hue = {
                          r: ((g - b) / delta) % 6,
                          g: ((b - r) / delta) + 2,
                          b: ((r - g) / delta) + 4,
                      }[c_max] * 60

            hue_line.append(hue)
            saturation_line.append(saturation)
            lightness_line.append(lightness)

        hue_data.append(hue_line)
        saturation_data.append(saturation_line)
        lightness_data.append(lightness_line)

    pixels = np.dstack((np.array(hue_data), np.array(saturation_data), np.array(lightness_data)))
    return pixels


def hsl_to_rgb(pixels):
    r_chanel = []
    g_chanel = []
    b_chanel = []

    h_chanel, s_chanel, l_chanel = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]

    for line in range(len(pixels)):
        r_line = []
        g_line = []
        b_line = []

        for col in range(len(pixels[line])):
            hue, saturation, lightness = h_chanel[line][col] / 360.0, s_chanel[line][col], l_chanel[line][col]

            if saturation == 0:
                r_line.append(int(lightness * 255))
                g_line.append(int(lightness * 255))
                b_line.append(int(lightness * 255))
            else:
                q = lightness * (1.0 + saturation) if lightness < 0.5 else lightness + saturation - lightness * saturation
                p = 2.0 * lightness - q

                r_line.append(int(hue_to_rgb(p, q, hue + 1 / 3) * 255))
                g_line.append(int(hue_to_rgb(p, q, hue) * 255))
                b_line.append(int(hue_to_rgb(p, q, hue - 1 / 3) * 255))

        r_chanel.append(r_line)
        g_chanel.append(g_line)
        b_chanel.append(b_line)

    pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2] = r_chanel, g_chanel, b_chanel
    return pixels


def hue_to_rgb(p, q, t):
    if t < 0:
        t += 1
    if t > 1:
        t -= 1
    if t < 1 / 6:
        return p + ((q - p) * 6.0 * t)
    if 1 / 6 <= t < 1 / 2:
        return q
    if 1 / 2 <= t < 2 / 3:
        return p + ((q - p) * (2 / 3 - t) * 6)
    return p
