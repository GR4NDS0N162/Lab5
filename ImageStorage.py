class ImageStorage:

    def __init__(self):
        self.known_images = {}  # Пример структуры для хранения известных образов

    def add_known_image(self, perceptual_hash, semantic_info):
        # Добавление известного образа в хранилище
        self.known_images[perceptual_hash] = semantic_info

    def get_semantic_info(self, perceptual_hash):
        # Получение семантической информации по перцептивному хэшу
        return self.known_images.get(perceptual_hash, None)
