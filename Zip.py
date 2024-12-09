import os
import zipfile

def compress_folder(folder_name, output_name):
    """
    특정 폴더를 ZIP 파일로 압축합니다.

    Args:
        folder_name (str): 압축할 폴더 이름
        output_name (str): 생성될 ZIP 파일 이름
    """
    # ZIP 파일 생성
    with zipfile.ZipFile(output_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_name):
            for file in files:
                file_path = os.path.join(root, file)
                # ZIP 파일에 파일 추가
                arcname = os.path.relpath(file_path, folder_name)  # 폴더 구조 보존
                zipf.write(file_path, arcname)
    print(f"{folder_name} 폴더가 {output_name}로 압축되었습니다.")

# 압축 실행
folder_to_compress = "videos"  # 압축할 폴더 이름
output_zip_name = "videos.zip"  # 생성될 ZIP 파일 이름

compress_folder(folder_to_compress, output_zip_name)
