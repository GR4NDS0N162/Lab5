import numpy as np
from PIL import Image

import Converters

MAX = 1
MEDIAN = 0
MIN = -1


class ImagePreprocessing:

    def __init__(self, step_window, contrast_factor, halftone_filter):
        self.step_window = step_window
        self.contrast_factor = contrast_factor
        self.halftone_filter = halftone_filter

    def process_image(self, image, show_image=False):
        pixels = np.array(image)

        pixels = self.adjust_contrast(pixels)
        if show_image:
            Image.fromarray(pixels).show()

        pixels = self.to_grayscale(pixels)
        if show_image:
            Image.fromarray(pixels).show()

        pixels = self.filter_max_min(pixels, self.halftone_filter)
        if show_image:
            Image.fromarray(pixels).show()

        pixels = self.to_mono(pixels)
        if show_image:
            Image.fromarray(pixels * 255).show()

        pixels = self.morphological_dilatation(pixels)
        if show_image:
            Image.fromarray(pixels * 255).show()

        pixels = 1 - pixels
        return pixels

    def adjust_contrast(self, pixels):
        pixels_hsl = Converters.rgb_to_hsl(pixels)

        lightness = pixels_hsl[:, :, 2]
        lightness = np.clip((lightness - 0.5) * self.contrast_factor + 0.5, 0, 1)

        pixels_hsl[:, :, 2] = lightness

        pixels = Converters.hsl_to_rgb(pixels_hsl)
        return pixels.astype(np.uint8)

    def to_grayscale(self, pixels):
        r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
        gray_pixels = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray_pixels.astype(np.uint8)

    def filter_max_min(self, pixels, mode):
        filtered_pixels = np.zeros((pixels.shape[0], pixels.shape[1]))

        for row in range(len(pixels)):
            for col in range(len(pixels[row])):
                window = pixels[max(0, row - self.step_window):min(pixels.shape[0], row + self.step_window + 1),
                         max(0, col - self.step_window):min(pixels.shape[1], col + self.step_window + 1)]

                if mode == MAX:
                    filtered_pixels[row][col] = np.max(window)
                elif mode == MIN:
                    filtered_pixels[row][col] = np.min(window)

        return filtered_pixels.astype(np.uint8)

    def to_mono(self, pixels):
        mean = np.mean(pixels)

        for row in range(len(pixels)):
            for col in range(len(pixels[row])):
                pixels[row][col] = 0 if pixels[row][col] < mean else 1

        return pixels

    def morphological_dilatation(self, pixels):
        return self.filter_max_min(pixels, MAX)

    def morphological_erosion(self, pixels):
        return self.filter_max_min(pixels, MIN)

    def morphological_closure(self, pixels):
        return self.morphological_erosion(self.morphological_dilatation(pixels))

    def gradiant(self, pixels):
        gradiant_pixels = np.logical_xor(self.morphological_dilatation(pixels), self.morphological_erosion(pixels))
        return gradiant_pixels
