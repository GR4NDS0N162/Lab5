from PIL import Image

import ImageAnalysis
import ImagePreprocessing
import ImageStorage

MAX = 1
MIN = -1

# Пример использования
if __name__ == "__main__":
    # Создание экземпляров модулей
    prep_module = ImagePreprocessing.ImagePreprocessing(step_window=1, contrast_factor=2, halftone_filter=MIN)
    analysis_module = ImageAnalysis.ImageAnalysis(16)
    storage_module = ImageStorage.ImageStorage()

    # Получение целевого изображения (предполагается, что image - это входное изображение)
    target_image = Image.open("images/Главная дорога.jpg").convert("RGB")

    # Модуль подготовки изображения
    processed_image = prep_module.process_image(target_image, True)

    # Модуль анализа изображения
    result_image = analysis_module.analyze_image(processed_image)

    # Пример добавления известного образа в хранилище
    perceptual_hash = "some_hash"
    semantic_info = "semantic_information"
    storage_module.add_known_image(perceptual_hash, semantic_info)

    # Пример получения семантической информации по перцептивному хэшу
    retrieved_info = storage_module.get_semantic_info(perceptual_hash)

    print("Semantic Information:", retrieved_info)
