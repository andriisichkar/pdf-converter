import os
import tkinter as tk
from tkinter import messagebox
from modules.image_converter import convert_images_to_pdf

class ImageOrderWindow:
    def __init__(self, parent, image_paths):
        self.top = tk.Toplevel(parent)
        self.top.title("Порядок зображень у PDF")
        self.image_paths = list(image_paths)
        self.result_pdf_path = None

        self._setup_window()
        self._create_widgets()
        self._populate_list()

    def _setup_window(self):
        window_width, window_height = 450, 350
        screen_width = self.top.winfo_screenwidth()
        screen_height = self.top.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.top.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.top.grab_set()

    def _create_widgets(self):
        label = tk.Label(self.top, text="Впорядкуйте зображення (верхнє = перша сторінка):", font=("Arial", 10))
        label.pack(pady=5)

        frame = tk.Frame(self.top)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode=tk.SINGLE, font=("Arial", 9))
        scrollbar.config(command=self.listbox.yview)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        btn_frame = tk.Frame(self.top)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        btn_up = tk.Button(btn_frame, text="▲ Вгору", width=10, command=self._move_up)
        btn_up.pack(side=tk.LEFT, padx=2)

        btn_down = tk.Button(btn_frame, text="▼ Вниз", width=10, command=self._move_down)
        btn_down.pack(side=tk.LEFT, padx=2)

        btn_remove = tk.Button(btn_frame, text="❌ Видалити", width=10, fg="red", command=self._remove_item)
        btn_remove.pack(side=tk.LEFT, padx=2)

        btn_save = tk.Button(
            self.top, 
            text="Зберегти в PDF", 
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 10, "bold"),
            command=self._generate_pdf
        )
        btn_save.pack(fill=tk.X, padx=10, pady=10)

    def _populate_list(self):
        self.listbox.delete(0, tk.END)
        for path in self.image_paths:
            self.listbox.insert(tk.END, os.path.basename(path))

    def _move_up(self):
        selected = self.listbox.curselection()
        if not selected or selected[0] == 0:
            return
        idx = selected[0]
        self.image_paths[idx], self.image_paths[idx - 1] = self.image_paths[idx - 1], self.image_paths[idx]
        self._populate_list()
        self.listbox.select_set(idx - 1)

    def _move_down(self):
        selected = self.listbox.curselection()
        if not selected or selected[0] == len(self.image_paths) - 1:
            return
        idx = selected[0]
        self.image_paths[idx], self.image_paths[idx + 1] = self.image_paths[idx + 1], self.image_paths[idx]
        self._populate_list()
        self.listbox.select_set(idx + 1)

    def _remove_item(self):
        selected = self.listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        del self.image_paths[idx]
        self._populate_list()

    def _generate_pdf(self):
        if not self.image_paths:
            messagebox.showwarning("Попередження", "Список зображень порожній!")
            return

        try:
            self.result_pdf_path = convert_images_to_pdf(self.image_paths)
            self.top.destroy()
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося створити PDF:\n{str(e)}")