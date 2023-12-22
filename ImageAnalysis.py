import numpy as np


class ImageAnalysis:

    def __init__(self, hash_dimension):
        self.hash_dimension = hash_dimension

    def analyze_image(self, processed_image):
        objects = self.detect_objects(processed_image)
        hashes, local_areas = self.compute_perceptual_hashes(objects)
        return hashes, local_areas

    def detect_objects(self, pixels):
        current_object = 0
        objects = {}
        for line in range(pixels.shape[0]):
            for col in range(pixels.shape[1]):

                if col - 1 < 0:
                    b = 0
                else:
                    b = pixels[line][col - 1]

                if line - 1 < 0:
                    c = 0
                else:
                    c = pixels[line - 1][col]

                a = pixels[line][col]

                if a == 0:
                    continue
                elif b == 0 and c == 0:
                    current_object += 1
                    pixels[line][col] = current_object
                    objects[current_object] = [[line, col]]
                elif b != 0 and c == 0:
                    pixels[line][col] = b
                    objects[b].append([line, col])
                elif b == 0 and c != 0:
                    pixels[line][col] = c
                    objects[c].append([line, col])
                elif b != 0 and c != 0:
                    if b == c:
                        pixels[line][col] = c
                        objects[c].append([line, col])
                    else:
                        min_i = min(b, c)
                        max_i = max(b, c)
                        pixels[line][col] = min_i
                        objects[min_i].append([line, col])
                        for pixel in objects[max_i]:
                            pixels[pixel[0]][pixel[1]] = min_i
                        objects[min_i].extend(objects[max_i])
                        objects.pop(max_i)

        individual_objects = []
        for object in objects:
            instance_object = np.zeros((pixels.shape[0], pixels.shape[1]), dtype=int)
            for line, col in objects[object]:
                instance_object[line][col] = 1
            individual_objects.append(instance_object)
        return np.array(individual_objects)

    def compute_perceptual_hashes(self, objects):
        perceptual_hashes = []
        local_areas = []

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

            local_areas.append([min_x, min_y, max_x, max_y])

            height = max_y - min_y + 1
            width = max_x - min_x + 1

            max_axis = max(height, width)

            def create_cropped_obj(target_size):
                cropped_object = np.zeros((target_size, target_size), dtype=int)
                object = objects[i][min_y:max_y + 1, min_x:max_x + 1]

                for y in range(object.shape[0]):
                    for x in range(object.shape[1]):
                        cropped_object[y][x] = object[y][x]

                return cropped_object

            if max_axis < self.hash_dimension:
                cropped_object = create_cropped_obj(max_axis)
                perceptual_hash = self.fit_to_hash(cropped_object, False)
            elif max_axis > self.hash_dimension:
                cropped_object = create_cropped_obj(max_axis)
                perceptual_hash = self.fit_to_hash(cropped_object, True)
            else:
                perceptual_hash = objects[i]

            perceptual_hash = perceptual_hash.ravel()
            perceptual_hash = int(''.join(map(str, perceptual_hash[:int(self.hash_dimension ** 2)])), 2)
            perceptual_hashes.append(format(perceptual_hash, f'0{int(self.hash_dimension ** 2) // 4}x'))

        return perceptual_hashes, local_areas

    def fit_to_hash(self, cropped_object, decrease):
        if cropped_object.shape[0] == self.hash_dimension:
            return cropped_object

        if decrease:
            perceptual_hash = self.downscale_hash(cropped_object, self.hash_dimension)
        else:
            perceptual_hash = self.upscale_hash(cropped_object, self.hash_dimension)

        return perceptual_hash

    def upscale_hash(self, cropped_object, size):
        perceptual_hash = np.zeros((size, size), dtype=int)
        step_window = size // cropped_object.shape[0]

        for y in range(cropped_object.shape[0]):
            for x in range(cropped_object.shape[1]):
                perceptual_hash[round(y * step_window):round(y * step_window + step_window + 1),
                round(x * step_window):round(x * step_window + step_window + 1)] = cropped_object[y][x]

        return np.array(perceptual_hash).astype(int)

    def downscale_hash(self, cropped_object, size):
        perceptual_hash = np.zeros((size, size), dtype=int)
        step_window = cropped_object.shape[0] // size

        for y in range(size):
            for x in range(size):
                window = cropped_object[round(y * step_window):round(y * step_window + step_window + 1),
                         round(x * step_window):round(x * step_window + step_window + 1)]
                perceptual_hash[y][x] = round(np.mean(window))

        return np.array(perceptual_hash).astype(int)
