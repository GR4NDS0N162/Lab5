import json

import numpy as np


class Pattern:

    def __init__(self, name, components):
        self.name = name
        self.components = components

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()

    def __str__(self):
        return self.name + ' - ' + str(self.components)


def get_binary_hash(hex_hash):
    binary_hash = bin(int(hex_hash, 16))[2:].zfill(len(hex_hash) * 4)
    return np.array(list(binary_hash), dtype=int)


class KnowledgeBase:

    def __init__(self, file_path, hash_dimension):
        self.file_path = file_path
        self.hash_dimension = hash_dimension
        self.hash_storage, self.pattern_storage = self.get_knowledge()

    def add_pattern(self, name, hashes):
        for i, perceptual_hash in enumerate(hashes):
            if perceptual_hash not in self.hash_storage:
                self.hash_storage.append(perceptual_hash)
        self.pattern_storage.append(Pattern(name, hashes))

    def database_search(self, perceptual_hash):
        result = []

        for pattern in self.pattern_storage:
            if perceptual_hash in pattern.components:
                result.append(str(pattern))

        return result

    def get_by_index(self, index):
        return self.pattern_storage[index]

    def compare_hashes(self, hash1, hash2, error):
        hash1 = get_binary_hash(hash1)
        hash2 = get_binary_hash(hash2)

        dif_hash = np.logical_xor(hash1, hash2)
        dif = np.count_nonzero(dif_hash) / (self.hash_dimension ** 2)

        if dif < error:
            return True
        else:
            return False

    def get_knowledge(self):
        with open(self.file_path, "r") as json_file:
            json_data = json.load(json_file)

        images = []
        for pattern in json_data["pattern_storage"]:
            images.append(Pattern(pattern['name'], pattern['components']))

        return json_data["hash_storage"], images

    def save_knowledge(self):
        with open(self.file_path, "w") as json_file:
            json.dump(self, json_file, default=lambda o: o.__dict__, indent=2)
