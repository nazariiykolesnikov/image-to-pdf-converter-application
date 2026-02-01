import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from PIL import Image
import os


class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.output_pdf_name = tk.StringVar()
        self.save_directory = ""
        self.selected_images_listbox = tk.Listbox(root, selectmode = tk.MULTIPLE)
        self.initialize_ui()

    def initialize_ui(self):
        title_label = tk.Label(self.root, text = "Images to PDF Converter Application", font = ("Helvetica", 16, "bold"))
        title_label.pack(pady = 10)
        select_images_button = tk.Button(self.root, text = "Select Images", command = self.select_images_for_create_pdf)
        select_images_button.pack(pady = (0, 10))
        self.selected_images_listbox.pack(pady = (0, 10), fill = tk.BOTH, expand = True)
        label = tk.Label(self.root, text = "Enter the PDF name to output:")
        label.pack()
        pdf_name_entry = tk.Entry(self.root, textvariable = self.output_pdf_name, width = 40, justify = 'center')
        pdf_name_entry.pack()
        select_folder_button = tk.Button(self.root, text = "Select Save Folder", command = self.select_save_folder)
        select_folder_button.pack(pady = (10, 10))
        convert_button = tk.Button(self.root, text = 'Convert to PDF', command = self.convert_images_to_pdf)
        convert_button.pack(pady = (20, 40))

    def select_images_for_create_pdf(self):
        self.image_paths = filedialog.askopenfilenames(
            title = 'Select images',
            filetypes = [("Image files", "*.png;*.jpg;*.jpeg")]
        )
        self.update_selected_images_listbox()

    def update_selected_images_listbox(self):
        self.selected_images_listbox.delete(0, tk.END)
        for image_path in self.image_paths:
            _, image_name = os.path.split(image_path)
            self.selected_images_listbox.insert(tk.END, image_name)

    def select_save_folder(self):
        self.save_directory = filedialog.askdirectory(title = "Select folder to save PDF")
        if self.save_directory:
            messagebox.showinfo("Folder Selected", f"PDF will be saved in: \n{self.save_directory}")

    def convert_images_to_pdf(self):
        if not self.image_paths:
            messagebox.showwarning("No Images", "Please, select images first")
            return

        pdf_name = self.output_pdf_name.get().strip()
        if not pdf_name:
            pdf_name = "output.pdf"
        elif not pdf_name.endswith(".pdf"):
            pdf_name += ".pdf"

        if self.save_directory:
            output_pdf_path = os.path.join(self.save_directory, pdf_name)
        else:
            output_pdf_path = pdf_name

        pdf = canvas.Canvas(output_pdf_path, pagesize = (612, 792))
        for image_path in self.image_paths:
            img = Image.open(image_path)
            available_width = 540
            available_height = 720
            scale_factor = min((available_width / img.width), (available_height / img.height))
            new_width = img.width * scale_factor
            new_height = img.height * scale_factor
            x_centered = (612 - new_width) / 2
            y_centered = (792 - new_height) / 2
            pdf.setFillColor(colors.white)
            pdf.rect(0, 0, 612, 792, fill = True)
            pdf.drawInlineImage(img, x_centered, y_centered, width = new_width, height = new_height)
            pdf.showPage()

        pdf.save()
        messagebox.showinfo("PDF successfully created", f"Your's PDF saved successfully: \n{output_pdf_path}")

def main():
    root = tk.Tk()
    root.title("Please, choose images to create PDF")
    converter = ImageToPDFConverter(root)
    root.geometry("400x600")
    root.mainloop()

if __name__ == "__main__":
    main()