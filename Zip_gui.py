import os
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox

def compress_folder(folder_name, output_name):
    """
    특정 폴더를 ZIP 파일로 압축합니다.

    Args:
        folder_name (str): 압축할 폴더 이름
        output_name (str): 생성될 ZIP 파일 이름
    """
    try:
        with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(folder_name):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, folder_name)  # 폴더 구조 보존
                    zipf.write(file_path, arcname)
        messagebox.showinfo("성공", f"{folder_name} 폴더가 {output_name}로 압축되었습니다.")
    except Exception as e:
        messagebox.showerror("에러", f"압축 중 에러가 발생했습니다: {e}")

def select_folder():
    """사용자가 압축할 폴더를 선택하도록 합니다."""
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)

def save_as_zip():
    """사용자가 ZIP 파일을 저장할 위치와 이름을 선택하도록 합니다."""
    file_selected = filedialog.asksaveasfilename(
        defaultextension=".zip",
        filetypes=[("ZIP 파일", "*.zip")],
        title="ZIP 파일 저장"
    )
    if file_selected:
        zip_path.set(file_selected)

def start_compression():
    """압축을 시작합니다."""
    folder = folder_path.get()
    zip_file = zip_path.get()
    if not folder or not zip_file:
        messagebox.showwarning("경고", "폴더와 ZIP 파일 이름을 모두 지정하세요.")
        return
    compress_folder(folder, zip_file)

# GUI 생성
root = tk.Tk()
root.title("폴더 압축기")

# 폴더 선택 UI
folder_path = tk.StringVar()
zip_path = tk.StringVar()

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

tk.Label(frame, text="압축할 폴더:").grid(row=0, column=0, sticky="w")
tk.Entry(frame, textvariable=folder_path, width=40).grid(row=0, column=1, padx=5)
tk.Button(frame, text="폴더 선택", command=select_folder).grid(row=0, column=2)

tk.Label(frame, text="ZIP 파일 저장:").grid(row=1, column=0, sticky="w")
tk.Entry(frame, textvariable=zip_path, width=40).grid(row=1, column=1, padx=5)
tk.Button(frame, text="저장 위치 선택", command=save_as_zip).grid(row=1, column=2)

tk.Button(frame, text="압축 시작", command=start_compression, bg="blue", fg="white").grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
