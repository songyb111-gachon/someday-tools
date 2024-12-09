import os
import re
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.VideoClip import ImageClip
from moviepy.editor import concatenate_videoclips  # 올바른 모듈에서 임포트
from PIL import Image, ImageDraw, ImageFont
import numpy as np


def get_sorted_video_files(folder_path):
    """
    폴더 내의 동영상 파일 목록을 가져와 숫자 순으로 정렬합니다.
    """
    print(f"Fetching video files from folder: {folder_path}")
    files = [f for f in os.listdir(folder_path) if f.startswith("rl-video-episode") and f.endswith(".mp4")]
    sorted_files = sorted(files, key=lambda x: int(re.search(r'(\d+)', x).group()))
    print(f"Sorted video files: {sorted_files}")
    return [os.path.join(folder_path, f) for f in sorted_files]


def create_text_image(text, video_size, font_size=24, font_color="white"):
    """
    텍스트 이미지를 생성합니다.
    """
    print(f"Creating text image for text: '{text}' with size: {video_size}")
    # 비디오 크기와 동일한 투명 배경 이미지 생성
    img = Image.new("RGBA", video_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 폰트 설정
    try:
        font_path = "C:\\Windows\\Fonts\\arial.ttf"  # 기본 폰트 경로
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    # 텍스트 크기 계산 및 위치 지정
    text_bbox = draw.textbbox((0, 0), text, font=font)  # 텍스트 경계 계산
    text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
    position = (video_size[0] - text_width - 10, 10)  # 오른쪽 상단
    draw.text(position, text, fill=font_color, font=font)

    return np.array(img)


def add_filename_overlay(video_path, filename):
    """
    주어진 비디오에 파일 이름을 텍스트 오버레이로 추가합니다.
    """
    print(f"Adding filename overlay for video: {video_path}, filename: {filename}")
    # 원본 영상 로드
    video = VideoFileClip(video_path)

    # 텍스트 이미지 생성
    try:
        text_img = create_text_image(filename, (video.w, video.h))
        text_clip = ImageClip(text_img, duration=video.duration)

        # 텍스트를 원본 영상에 합성
        composite = CompositeVideoClip([video, text_clip])
        print(f"Overlay added successfully for {filename}")
        return composite
    except Exception as e:
        print(f"Error adding overlay for {filename}: {e}")
        return video  # 텍스트 없이 원본 영상 반환


def merge_videos(folder_path, output_path):
    """
    폴더 내 동영상을 정렬하고 합친 후 출력 파일로 저장합니다.
    """
    print(f"Starting video merge. Folder: {folder_path}, Output: {output_path}")
    # 숫자 순으로 정렬된 파일 목록 가져오기
    sorted_files = get_sorted_video_files(folder_path)
    video_clips = []

    for file in sorted_files:
        filename = os.path.basename(file)  # 파일 이름 추출
        print(f"Processing video: {file}")
        video_with_text = add_filename_overlay(file, filename)
        video_clips.append(video_with_text)

    # 동영상 클립 병합
    print(f"Merging {len(video_clips)} video clips.")
    try:
        final_video = concatenate_videoclips(video_clips, method="compose")
        print(f"Writing final video to {output_path}")
        final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
        print("Video merge completed successfully.")
    except Exception as e:
        print(f"Error during video merge: {e}")


# 실행
if __name__ == "__main__":
    folder_path = "videos-PPO"  # 영상이 있는 폴더 경로
    output_path = "videos-PPO.mp4"  # 출력 영상 파일 경로
    merge_videos(folder_path, output_path)
