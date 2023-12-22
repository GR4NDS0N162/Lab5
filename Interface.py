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
        self.add_to_database_button.grid(row=1, column=2, columnspan=3)

        self.notification_label = tk.Message(self.root, text="", fg="green", width=500)
        self.notification_label.grid(row=3, column=0, columnspan=5)

        self.hash_dimension = 16
        self.prep_module = ImagePreprocessing.ImagePreprocessing(step_window=1, contrast_change_factor=2,
                                                                 halftone_filter=ImagePreprocessing.MIN)
        self.analysis_module = ImageAnalysis.ImageAnalysis(hash_dimension=self.hash_dimension)
        self.knowledge_base = KnowledgeBase.KnowledgeBase(file_path="data.json", hash_dimension=self.hash_dimension)

        hash_option_list = self.knowledge_base.hash_storage
        hash_variable = tk.StringVar(self.root)
        hash_variable.set(hash_option_list[0])
        hash_variable.trace("w", self.on_hash_option_click)

        self.dropdown_hashes = tk.OptionMenu(self.root, hash_variable, *hash_option_list)
        self.dropdown_hashes.grid(row=4, column=1, columnspan=4)

        self.hashes_info = tk.Message(self.root, text="", fg="black", width=500)
        self.hashes_info.grid(row=5, column=0, columnspan=5)

        index_option_list = list(map(str, range(len(self.knowledge_base.pattern_storage))))
        index_variable = tk.StringVar(self.root)
        index_variable.set(index_option_list[0])
        index_variable.trace("w", self.on_index_option_click)

        self.dropdown_hashes = tk.OptionMenu(self.root, index_variable, *index_option_list)
        self.dropdown_hashes.grid(row=4, column=0, columnspan=1)

        self.target_image = None
        self.knowledge_base_changed = False

    def on_hash_option_click(self, *args):
        variable = self.dropdown_hashes.getvar(args[0])
        result = self.knowledge_base.database_search(variable)
        self.hashes_info.configure(text=str(result))

    def on_index_option_click(self, *args):
        variable = self.dropdown_hashes.getvar(args[0])
        pattern = self.knowledge_base.get_by_index(int(variable))
        self.hashes_info.configure(text=str(pattern))

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
            hashes = self.analysis_module.analyze_image(processed_image)
            self.target_image = {"name": name, "hashes": hashes}
            self.show_notification(f"Вычисленные хеши: {str(hashes)}")
        except Exception as e:
            self.show_notification(f"Ошибка при вычислении хеша: {str(e)}", "red")

    def add_to_database(self):
        self.knowledge_base_changed = True
        self.knowledge_base.add_pattern(self.target_image['name'], self.target_image['hashes'])
        self.show_notification(f"Добавлено в базу: {self.target_image['name']}")

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
