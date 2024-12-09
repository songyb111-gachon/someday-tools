import os
import re
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips


def get_sorted_video_files(folder_path):
    # 파일 목록 가져오기
    files = [f for f in os.listdir(folder_path) if f.startswith("rl-video-episode") and f.endswith(".mp4")]

    # 숫자 순으로 정렬
    sorted_files = sorted(files, key=lambda x: int(re.search(r'(\d+)', x).group()))
    return sorted_files


def add_filename_overlay(video_path, filename):
    # 원본 영상 로드
    video = VideoFileClip(video_path)

    # 텍스트 오버레이 생성
    text = TextClip(filename, fontsize=24, color='white').set_position(('right', 'top')).set_duration(video.duration)

    # 텍스트를 원본 영상에 합성
    composite = CompositeVideoClip([video, text])
    return composite


def merge_videos(folder_path, output_path):
    sorted_files = get_sorted_video_files(folder_path)
    video_clips = []

    for file in sorted_files:
        full_path = os.path.join(folder_path, file)
        video_with_text = add_filename_overlay(full_path, file)
        video_clips.append(video_with_text)

    # 영상 병합
    final_video = concatenate_videoclips(video_clips, method="compose")
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")


# 실행
folder_path = "YOUR_FOLDER_PATH"  # 영상이 있는 폴더 경로
output_path = "output_video.mp4"  # 출력 영상 파일 경로
merge_videos(folder_path, output_path)
