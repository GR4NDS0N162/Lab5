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

        return hashes
