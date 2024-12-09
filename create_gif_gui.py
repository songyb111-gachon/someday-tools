import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image
import os
from datetime import datetime


def create_gif(image_files, output_gif_path, duration=600):
    images = []
    max_width = 0
    max_height = 0

    # 첫 번째 이미지를 확인하여 최대 크기를 계산
    for image_file in image_files:
        if os.path.exists(image_file):
            image = Image.open(image_file)
            max_width = max(max_width, image.width)
            max_height = max(max_height, image.height)
        else:
            print(f"파일이 존재하지 않습니다: {image_file}")
            return

    # 각 이미지를 열고 크기를 맞추고, 작은 이미지는 중앙에 배치
    for image_file in image_files:
        if os.path.exists(image_file):
            image = Image.open(image_file)
            new_image = Image.new("RGBA", (max_width, max_height), (255, 255, 255, 0))  # 투명 배경
            offset = ((max_width - image.width) // 2, (max_height - image.height) // 2)
            new_image.paste(image, offset)
            images.append(new_image)
        else:
            print(f"파일이 존재하지 않습니다: {image_file}")
            return

    # 첫 번째 이미지에서 GIF로 저장
    images[0].save(output_gif_path, save_all=True, append_images=images[1:], duration=duration, loop=0)
    print(f"GIF 파일이 저장되었습니다: {output_gif_path}")


def select_images():
    files = filedialog.askopenfilenames(
        title="Select Images",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff;*.gif")],
    )
    for file in files:
        images_listbox.insert(tk.END, file)


def remove_selected_image():
    selected = images_listbox.curselection()
    for index in reversed(selected):
        images_listbox.delete(index)


def move_image_up():
    selected = images_listbox.curselection()
    for index in selected:
        if index > 0:
            item = images_listbox.get(index)
            images_listbox.delete(index)
            images_listbox.insert(index - 1, item)
            images_listbox.select_set(index - 1)


def move_image_down():
    selected = images_listbox.curselection()
    for index in reversed(selected):
        if index < images_listbox.size() - 1:
            item = images_listbox.get(index)
            images_listbox.delete(index)
            images_listbox.insert(index + 1, item)
            images_listbox.select_set(index + 1)


def generate_gif():
    image_files = list(images_listbox.get(0, tk.END))
    if not image_files:
        messagebox.showerror("Error", "No images selected!")
        return

    output_gif_path = filedialog.asksaveasfilename(
        title="Save GIF As", defaultextension=".gif", filetypes=[("GIF Files", "*.gif")]
    )
    if output_gif_path:
        try:
            duration = simpledialog.askinteger("GIF Duration", "Enter duration between frames (ms):", minvalue=100, maxvalue=5000)
            if duration is None:
                return
            create_gif(image_files, output_gif_path, duration)
            messagebox.showinfo("Success", f"GIF saved successfully: {output_gif_path}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


# Create the main GUI window
root = tk.Tk()
root.title("Image to GIF Converter")

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

generate_btn = tk.Button(root, text="Generate GIF", command=generate_gif)
generate_btn.pack(pady=10)

# Run the GUI event loop
root.mainloop()
