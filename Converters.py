import numpy as np


def rgb_to_hsl(pixels):
    hue = []
    saturation = []
    lightness = []
    r_chanel, g_chanel, b_chanel = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
    for line in range(len(pixels)):
        hue_line = []
        saturation_line = []
        lightness_line = []
        for col in range(len(pixels[line])):
            r, g, b = r_chanel[line][col] / 255.0, g_chanel[line][col] / 255.0, b_chanel[line][col] / 255.0
            max_s = max(r, g, b)
            min_s = min(r, g, b)
            l = (max_s + min_s) / 2.0

            if max_s == min_s:
                h = s = 0.0
            else:
                d = max_s - min_s
                s = d / (2.0 - max_s - min_s) if l > 0.5 else d / (max_s + min_s)
                h = {
                        r: (g - b) / d + (360.0 if g < b else 0.0),
                        g: (b - r) / d + 120.0,
                        b: (r - g) / d + 240.0,
                    }[max_s] % 6.0

            hue_line.append(h * 60)
            saturation_line.append(s)
            lightness_line.append(l)

        hue.append(hue_line)
        saturation.append(saturation_line)
        lightness.append(lightness_line)

    pixels = np.dstack((np.array(hue), np.array(saturation), np.array(lightness)))
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
            h, s, l = h_chanel[line][col] / 360.0, s_chanel[line][col], l_chanel[line][col]

            if s == 0:
                r_line.append(int(l * 255))
                g_line.append(int(l * 255))
                b_line.append(int(l * 255))
            else:
                q = l * (1.0 + s) if l < 0.5 else l + s - l * s
                p = 2.0 * l - q

                r_line.append(int(hue_to_rgb(p, q, h + 1 / 3) * 255))
                g_line.append(int(hue_to_rgb(p, q, h) * 255))
                b_line.append(int(hue_to_rgb(p, q, h - 1 / 3) * 255))

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
