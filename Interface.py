import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from pathlib import Path

import ImagePreprocessing
import ImageAnalysis
import KnowledgeBase


class ImageDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Database App")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.root.resizable(False, False)
        self.image_path_entry = tk.Entry(self.root, width=40)
        self.image_path_entry.grid(row=0, column=0, padx=10, pady=10)

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_image)
        self.browse_button.grid(row=0, column=1, padx=10, pady=10)

        self.calculate_hash_button = tk.Button(self.root, text="Calculate Hash", command=self.calculate_hash)
        self.calculate_hash_button.grid(row=0, column=2, padx=10, pady=10)

        self.add_to_database_button = tk.Button(self.root, text="Add to Database", command=self.add_to_database)
        self.add_to_database_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.search_similar_button = tk.Button(self.root, text="Search Similar Images", command=self.search_likeness)
        self.search_similar_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.notification_label = tk.Label(self.root, text="", fg="green")
        self.notification_label.grid(row=3, column=0, columnspan=2, pady=10)

        self.prep_module = ImagePreprocessing.ImagePreprocessing(step_window=1, contrast_factor=2,
                                                                 halftone_filter=ImagePreprocessing.MIN)
        self.analysis_module = ImageAnalysis.ImageAnalysis(hash_dimension=16)
        self.knowledge_base = KnowledgeBase.KnowledgeBase("data.json")

        self.target_image = None
        self.knowledge_base_changed = False

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
            self.show_notification(f"Орёл в гнезде!!")
        except Exception as e:
            self.show_notification(f"Error calculating hash: {str(e)}", "red")

    def add_to_database(self):
        self.knowledge_base_changed = True
        result = self.knowledge_base.add_likeness(self.target_image['name'], self.target_image['hashes'],
                                                  self.target_image['local_areas'])
        if result:
            self.show_notification(f"Added to database: {self.target_image['name']}")
        else:
            self.show_notification(f"This image already exists!!!", "red")

    def search_likeness(self):
        result = self.knowledge_base.database_search(self.target_image)
        if result is None:
            self.show_notification(f"Search results: {result}", "red")
        self.show_notification(f"Search results: {result}")

    def show_notification(self, message, color="green"):
        self.notification_label.config(text=message, fg=color)

    def on_closing(self):
        if self.knowledge_base_changed and messagebox.askokcancel(f"f{self.knowledge_base.file_path}*",
                                                                  "Сохранить изменения в базе знаний?"):
            self.knowledge_base.safe_knowledge()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageDatabaseApp(root)
    root.mainloop()
