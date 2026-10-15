import tkinter as tk
from tkinter import filedialog, messagebox
from modules.word_converter import convert_word_to_pdf
from gui.image_order_window import ImageOrderWindow

class AppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Конвертер")
        self._setup_window()
        self._create_widgets()

    def _setup_window(self):
        window_width, window_height = 360, 200
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(False, False)

    def _create_widgets(self):
        label = tk.Label(self.root, text="Оберіть потрібну дію:", font=("Arial", 12, "bold"), pady=15)
        label.pack()

        btn_word = tk.Button(
            self.root,
            text="📄 Word (DOCX) -> PDF",
            font=("Arial", 10),
            width=28,
            height=2,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            command=self._handle_word_conversion
        )
        btn_word.pack(pady=5)

        btn_img = tk.Button(
            self.root,
            text="🖼️ Зображення (JPG/PNG) -> PDF",
            font=("Arial", 10),
            width=28,
            height=2,
            bg="#2196F3",
            fg="white",
            activebackground="#0b7dda",
            command=self._handle_image_conversion
        )
        btn_img.pack(pady=5)

    def _handle_word_conversion(self):
        file_path = filedialog.askopenfilename(
            title="Оберіть файл Word",
            filetypes=[("Word Documents", "*.docx *.doc")]
        )
        if not file_path:
            return

        try:
            pdf_path = convert_word_to_pdf(file_path)
            messagebox.showinfo("Успіх!", f"Файл успішно збережено:\n{pdf_path}")
        except Exception as e:
            messagebox.showerror("Помилка", f"Сталася помилка при конвертації Word:\n{str(e)}")

    def _handle_image_conversion(self):
        file_paths = filedialog.askopenfilenames(
            title="Оберіть зображення",
            filetypes=[("Зображення", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp")]
        )
        if not file_paths:
            return

        order_window = ImageOrderWindow(self.root, file_paths)
        self.root.wait_window(order_window.top)

        if order_window.result_pdf_path:
            messagebox.showinfo("Успіх!", f"PDF успішно створено:\n{order_window.result_pdf_path}")

    def run(self):
        self.root.mainloop()