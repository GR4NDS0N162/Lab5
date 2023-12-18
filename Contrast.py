import numpy as np


def stretch(pixels):
    min_val = np.min(pixels[pixels > 13])
    max_val = np.max(pixels[pixels < 242])
    difference = max_val - min_val
    for line in range(len(pixels)):
        for pixel in range(len(pixels[line])):
            pixels[line][pixel] = int(((pixels[line][pixel] - min_val) / difference) * 255)
    return pixels


def equalization(pixels):
    frequency = {i: 0 for i in range(256)}

    for line in range(len(pixels)):
        for pixel in range(len(pixels[line])):
            intensity = int(pixels[line][pixel] * 255)

            if intensity in frequency:
                frequency[intensity] += 1
            else:
                frequency[intensity] = 1

    intensity_frequencies = [frequency[key] for key in sorted(frequency.keys())]

    cumulative_sum = 0

    cdf = []
    for intensity_frequency in intensity_frequencies:
        cumulative_sum += intensity_frequency
        cdf.append(cumulative_sum)

    minCDF = cdf[0]
    maxCDF = cdf[-1]

    normalizedCDF = []

    for value in cdf:
        normalizedCDF.append((value - minCDF) / (maxCDF - minCDF))

    for line in range(len(pixels)):
        for pixel in range(len(pixels[line])):
            pixels[line][pixel] = normalizedCDF[int(pixels[line][pixel] * 255)]

    return pixels


def increase_contrast_manually(pixels, factor):
    for line in range(len(pixels)):
        for col in range(len(pixels[line])):
            pixels[line][col] = (int((pixels[line][col][0] - 128) * factor + 128),
                                 int((pixels[line][col][1] - 128) * factor + 128),
                                 int((pixels[line][col][2] - 128) * factor + 128))

    return pixels
