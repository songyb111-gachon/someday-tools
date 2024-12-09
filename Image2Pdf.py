import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
from PIL import Image
from reportlab.pdfgen import canvas


def convert_images_to_pdf_with_original_aspect(image_files, output_pdf):
    """
    Convert a list of images to a single PDF with each image preserving its aspect ratio.

    :param image_files: List of paths to image files.
    :param output_pdf: Path to the output PDF file.
    """
    c = canvas.Canvas(output_pdf)

    for image_file in image_files:
        img = Image.open(image_file)

        # Get image dimensions
        width, height = img.size

        # Convert pixels to points (1 point = 1/72 inch)
        width_pt = width * 0.75
        height_pt = height * 0.75

        # Set the page size to the image size
        c.setPageSize((width_pt, height_pt))

        # Draw the image at the bottom-left corner (0, 0)
        c.drawImage(image_file, 0, 0, width_pt, height_pt)

        # Finish the current page
        c.showPage()

    # Save the PDF
    c.save()
    print(f"PDF saved successfully: {output_pdf}")


def select_images():
    """
    Open a file dialog to select image files and add them to the list.
    """
    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.gif")],
    )
    for file in files:
        images_listbox.insert(tk.END, file)


def remove_selected_image():
    """
    Remove the selected image from the list.
    """
    selected = images_listbox.curselection()
    for index in reversed(selected):
        images_listbox.delete(index)


def move_image_up():
    """
    Move the selected image up in the list.
    """
    selected = images_listbox.curselection()
    for index in selected:
        if index > 0:
            item = images_listbox.get(index)
            images_listbox.delete(index)
            images_listbox.insert(index - 1, item)
            images_listbox.select_set(index - 1)


def move_image_down():
    """
    Move the selected image down in the list.
    """
    selected = images_listbox.curselection()
    for index in reversed(selected):
        if index < images_listbox.size() - 1:
            item = images_listbox.get(index)
            images_listbox.delete(index)
            images_listbox.insert(index + 1, item)
            images_listbox.select_set(index + 1)


def generate_pdf():
    """
    Generate a PDF from the images in the list.
    """
    image_files = list(images_listbox.get(0, tk.END))
    if not image_files:
        messagebox.showerror("Error", "No images selected!")
        return

    output_pdf = filedialog.asksaveasfilename(
        title="Save PDF As", defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")]
    )
    if output_pdf:
        convert_images_to_pdf_with_original_aspect(image_files, output_pdf)
        messagebox.showinfo("Success", f"PDF saved successfully: {output_pdf}")


# Create the main GUI window
root = tk.Tk()
root.title("Image to PDF Converter")

# Create a frame for the listbox and scrollbar
frame = tk.Frame(root)
frame.pack(pady=10)

# Create a listbox to display selected images
images_listbox = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=60, height=15)
images_listbox.pack(side=tk.LEFT, padx=5)

# Add a scrollbar to the listbox
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=images_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
images_listbox.config(yscrollcommand=scrollbar.set)

# Add buttons for image selection and manipulation
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

select_btn = tk.Button(btn_frame, text="Select Images", command=select_images)
select_btn.grid(row=0, column=0, padx=5)

remove_btn = tk.Button(btn_frame, text="Remove Selected", command=remove_selected_image)
remove_btn.grid(row=0, column=1, padx=5)

up_btn = tk.Button(btn_frame, text="Move Up", command=move_image_up)
up_btn.grid(row=0, column=2, padx=5)

down_btn = tk.Button(btn_frame, text="Move Down", command=move_image_down)
down_btn.grid(row=0, column=3, padx=5)

generate_btn = tk.Button(root, text="Generate PDF", command=generate_pdf)
generate_btn.pack(pady=10)

# Run the GUI event loop
root.mainloop()
