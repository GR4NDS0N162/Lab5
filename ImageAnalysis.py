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
        # TODO: Нужно реализовать.
        return hashes
