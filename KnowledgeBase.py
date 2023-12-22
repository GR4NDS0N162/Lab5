import json
from itertools import product

import numpy as np

import Connection


class Pattern:

    def __init__(self, name, components):
        self.name = name
        self.components = components

    def __eq__(self, other):
        return self.name.lower() == other.name.lower()


def get_binary_hash(hex_hash):
    binary_hash = bin(int(hex_hash, 16))[2:].zfill(len(hex_hash) * 4)
    return np.array(list(binary_hash), dtype=int)


class KnowledgeBase:

    def __init__(self, file_path, hash_dimension):
        self.file_path = file_path
        self.hash_dimension = hash_dimension
        self.hash_storage, self.pattern_storage = self.get_knowledge()

    def add_pattern(self, name, hashes):
        for i, component in enumerate(hashes):
            not_changed = True
            for component_stor in self.hash_storage:
                if self.compare_hashes(component, component_stor, 0.1):
                    hashes[i] = component_stor
                    not_changed = False
                    break

            if not_changed:
                self.hash_storage.append(component)

        self.pattern_storage.append(Pattern(name, hashes))
        return True

    def database_search(self, target_image):
        known_objects = dict()
        for i, hash in enumerate(target_image['hashes']):
            for hash_stor in self.hash_storage:
                if self.compare_hashes(hash, hash_stor, 0.2):
                    if hash_stor in known_objects:
                        known_objects[hash_stor].append(i)
                    else:
                        known_objects[hash_stor] = [i]

        if len(known_objects) == 0:
            return None

        result = []
        for likeness in self.pattern_storage:
            check = False
            for component in likeness.components:
                if component not in known_objects:
                    check = True
                    break

            if check:
                continue

            arrays = []
            for component in likeness.components:
                arrays.append(known_objects[component])

            all_combinations = list(product(*arrays))
            for combin in all_combinations:
                local_areas = [target_image['local_areas'][i] for i in combin]
                connections = Connection.get_connections(likeness.components, local_areas)
                if connections == likeness.connections:
                    result.append(likeness.name)

        if len(result) == 0:
            return None

        return result

    def compare_hashes(self, hash1, hash2, accuracy):
        hash1 = get_binary_hash(hash1)
        hash2 = get_binary_hash(hash2)

        dif_hash = np.logical_xor(hash1, hash2)
        dif = np.count_nonzero(dif_hash)
        if dif / (self.hash_dimension ** 2) < accuracy:
            return True
        else:
            return False

    def get_knowledge(self):
        with open(self.file_path, "r") as json_file:
            json_data = json.load(json_file)

        images = []
        for likeness in json_data["pattern_storage"]:
            images.append(Pattern(likeness['name'], likeness['components']))

        return json_data["hash_storage"], images

    def save_knowledge(self):
        with open(self.file_path, "w") as json_file:
            json.dump(self, json_file, default=lambda o: o.__dict__, indent=2)
