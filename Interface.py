import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox

from PIL import Image

import ImageAnalysis
import ImagePreprocessing
import KnowledgeBase


class ImageDatabaseApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Приложение")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.resizable(False, False)
        self.image_path_entry = tk.Entry(self.root, width=50)
        self.image_path_entry.grid(row=0, column=0, columnspan=4)

        self.browse_button = tk.Button(self.root, text="Обзор", command=self.browse_image)
        self.browse_button.grid(row=0, column=4, columnspan=1)

        self.calculate_hash_button = tk.Button(self.root, text="Вычислить хеш", command=self.calculate_hash)
        self.calculate_hash_button.grid(row=1, column=0, columnspan=2)

        self.add_to_database_button = tk.Button(self.root, text="Добавить в хранилище", command=self.add_to_database)
        self.add_to_database_button.grid(row=1, column=1, columnspan=3)

        self.notification_label = tk.Label(self.root, text="", fg="green")
        self.notification_label.grid(row=3, column=0, columnspan=5)

        self.hash_dimension = 16
        self.prep_module = ImagePreprocessing.ImagePreprocessing(step_window=1, contrast_change_factor=2,
                                                                 halftone_filter=ImagePreprocessing.MIN)
        self.analysis_module = ImageAnalysis.ImageAnalysis(hash_dimension=self.hash_dimension)
        self.knowledge_base = KnowledgeBase.KnowledgeBase(file_path="data.json", hash_dimension=self.hash_dimension)

        option_list = self.knowledge_base.hash_storage
        variable = tk.StringVar(self.root)
        variable.set(option_list[0])
        variable.trace("w", self.on_hash_option_click)

        self.dropdown_hashes = tk.OptionMenu(self.root, variable, *option_list)
        self.dropdown_hashes.grid(row=4, column=0, columnspan=5)

        self.dropdown_hashes_info = tk.Message(self.root, text="", fg="black", width=400)
        self.dropdown_hashes_info.grid(row=5, column=0, columnspan=5)

        self.target_image = None
        self.knowledge_base_changed = False

    def on_hash_option_click(self, *args):
        variable = self.dropdown_hashes.getvar(args[0])
        result = self.knowledge_base.database_search(variable)
        self.dropdown_hashes_info.configure(text=str(result))

    def browse_image(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            self.image_path_entry.delete(0, tk.END)
            self.image_path_entry.insert(0, file_path)

    def calculate_hash(self):
        image_path = self.image_path_entry.get()
        try:
            name = Path(image_path).stem
            image = Image.open(image_path).convert("RGB")
            processed_image = self.prep_module.process_image(image)
            hashes, local_areas = self.analysis_module.analyze_image(processed_image)
            self.target_image = {"name": name, "hashes": hashes, "local_areas": local_areas}
            self.show_notification(f"Успешно вычислен хеш!")
        except Exception as e:
            self.show_notification(f"Ошибка при вычислении хеша: {str(e)}", "red")

    def add_to_database(self):
        self.knowledge_base_changed = True
        result = self.knowledge_base.add_pattern(self.target_image['name'], self.target_image['hashes'])
        if result:
            self.show_notification(f"Добавлено в базу: {self.target_image['name']}")
        else:
            self.show_notification(f"Это изображение уже есть!", "red")

    def show_notification(self, message, color="green"):
        self.notification_label.config(text=message, fg=color)

    def on_closing(self):
        if self.knowledge_base_changed and messagebox.askokcancel(f"f{self.knowledge_base.file_path}*",
                                                                  "Сохранить изменения в базе знаний?"):
            self.knowledge_base.save_knowledge()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDatabaseApp(root)
    root.mainloop()
