import numpy as np

import Converters

MAX = 1
MEDIAN = 0
MIN = -1


class ImagePreprocessing:

    def __init__(self, step_window, contrast_factor, halftone_filter):
        self.step_window = step_window
        self.contrast_factor = contrast_factor
        self.halftone_filter = halftone_filter

    def process_image(self, image):
        pixels = np.array(image)
        pixels = self.adjust_contrast(pixels)
        pixels = self.grayscale_filter(pixels)
        pixels = self.filter_median_max_min(pixels, self.halftone_filter)
        pixels = self.filter_mono(pixels)
        pixels = self.dilate(pixels)
        return pixels

    def adjust_contrast(self, pixels):
        pixels_hsl = Converters.rgb_to_hsl(pixels)

        lightness = pixels_hsl[:, :, 2]
        lightness = np.clip((lightness - 0.5) * self.contrast_factor + 0.5, 0, 1)

        pixels_hsl[:, :, 2] = lightness

        pixels = Converters.hsl_to_rgb(pixels_hsl)
        return pixels.astype(int)

    def grayscale_filter(self, pixels):
        r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
        gray_pixels = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray_pixels.astype(int)

    def filter_median_max_min(self, pixels, mode):
        filtered_pixels = np.zeros((pixels.shape[0], pixels.shape[1]))
        for line in range(len(pixels)):
            for col in range(len(pixels[line])):
                window = pixels[max(0, line - self.step_window):min(pixels.shape[0], line + self.step_window + 1),
                         max(0, col - self.step_window):min(pixels.shape[1], col + self.step_window + 1)]

                if mode == MAX:
                    filtered_pixels[line][col] = np.max(window)
                elif mode == MEDIAN:
                    filtered_pixels[line][col] = np.median(window)
                elif mode == MIN:
                    filtered_pixels[line][col] = np.min(window)

        # image = Image.fromarray(filtered_pixels)
        # image.show()
        return filtered_pixels

    def filter_mono(self, pixels):
        mean = np.mean(pixels)
        for line in range(len(pixels)):
            for col in range(len(pixels[line])):
                pixels[line][col] = 1 if pixels[line][col] < mean else 0

        # mono_image = Image.fromarray(pixels)
        # mono_image.show()
        return pixels

    def dilate(self, pixels):
        return self.filter_median_max_min(pixels, MAX)

    def erode(self, pixels):
        return self.filter_median_max_min(pixels, MIN)

    def closing(self, pixels):
        return self.erode(self.dilate(pixels))

    def gradiant(self, pixels):
        gradiant_pixels = np.logical_xor(self.dilate(pixels), self.erode(pixels))
        # gradiant_image = Image.fromarray(gradiant_pixels)
        # gradiant_image.show()
        return gradiant_pixels
