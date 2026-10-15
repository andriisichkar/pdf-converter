import os
from datetime import datetime
from typing import List
from PIL import Image

def convert_images_to_pdf(image_paths: List[str]) -> str:
    """
    Конвертує список зображень у єдиний PDF-файл.
    Автоматично зберігає файл у папку з першим зображенням 
    і додає дату та час у назву.
    Повертає шлях до створеного PDF.
    """
    if not image_paths:
        raise ValueError("Не обрано жодного зображення для конвертації.")

    images = []
    for path in image_paths:
        img = Image.open(path)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        images.append(img)

    # 1. Беремо директорію першого зображення
    first_image_dir = os.path.dirname(image_paths[0])

    # 2. Формуємо дату та час: РРРРММДД_ГГХХСС (наприклад, 20261015_194530)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"image_to_pdf_{timestamp}.pdf"

    # 3. Підсумковий шлях для збереження
    save_path = os.path.join(first_image_dir, pdf_filename)

    # Зберігаємо PDF
    images[0].save(save_path, save_all=True, append_images=images[1:])
    return save_path