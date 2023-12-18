import numpy as np


class ImageAnalysis:

    def __init__(self, hash_dimension):
        self.hash_dimension = hash_dimension

    def analyze_image(self, processed_image):
        objects = self.detect_objects(processed_image)
        hashes = np.zeros((objects.shape[0], self.hash_dimension, self.hash_dimension))
        hashes = self.compute_perceptual_hashes(objects, hashes)

    def detect_objects(self, image):
        return np.array([image])  # TODO: Стоит заглушка, нужно реализовать.

    def compute_perceptual_hashes(self, objects, hashes):
        for i in range(objects.shape[0]):
            min_y = objects.shape[1]
            min_x = objects.shape[2]
            max_y = 0
            max_x = 0

            for y in range(objects.shape[1]):
                for x in range(objects.shape[2]):
                    min_x = min(x, min_x) if objects[i][y][x] else min_x
                    min_y = min(y, min_y) if objects[i][y][x] else min_y
                    max_x = max(x, max_x) if objects[i][y][x] else max_x
                    max_y = max(y, max_y) if objects[i][y][x] else max_y

            height = max_y - min_y + 1
            width = max_x - min_x + 1

            max_axis = max(height, width)

            cropped_object = np.zeros((max_axis, max_axis))
            for y in range(height):
                for x in range(width):
                    cropped_object[y][x] = objects[i][min_y + y][min_x + x]

            scale = max_axis / self.hash_dimension

            for y in range(hashes.shape[1]):
                for x in range(hashes.shape[2]):
                    x_start = round(scale * x)
                    x_end = round(scale * (x + 1))
                    y_start = round(scale * y)
                    y_end = round(scale * (y + 1))

                    bit_sum = 0
                    bit_count = 0
                    for y_bit in range(y_start, y_end):
                        for x_bit in range(x_start, x_end):
                            bit_sum += cropped_object[y_bit][x_bit]
                            bit_count += 1
                    bit = bit_sum / bit_count

                    hashes[i][y][x] = 0 if bit < 0.5 else 1

        return hashes
