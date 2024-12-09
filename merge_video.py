import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip


def merge_videos_with_filenames(folder_path, output_filename):
    """
    특정 폴더의 영상을 순차적으로 합치고 각 원본 영상 이름을 우측 상단에 표시합니다.

    Args:
        folder_path (str): 영상이 저장된 폴더 경로
        output_filename (str): 생성될 출력 파일 이름
    """
    # 폴더 내 영상 파일 정렬
    video_files = sorted(
        [f for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mov'))],
        key=lambda x: int(x.split('-')[-1].split('.')[0])  # 숫자 기반 정렬
    )

    clips = []
    for video_file in video_files:
        video_path = os.path.join(folder_path, video_file)
        clip = VideoFileClip(video_path)

        # 영상 이름 텍스트 생성
        text = TextClip(video_file, fontsize=24, color='white', bg_color='black')
        text = text.set_duration(clip.duration).set_position(("right", "top"))

        # 텍스트와 영상을 합성
        composite = CompositeVideoClip([clip, text])
        clips.append(composite)

    # 영상 병합
    final_clip = concatenate_videoclips(clips, method="compose")

    # 최종 영상 출력
    final_clip.write_videofile(output_filename, codec="libx264", fps=24)
    print(f"영상이 {output_filename}로 저장되었습니다.")


# 실행 예제
folder_path = "./videos"  # 영상 폴더 경로
output_filename = "merged_video.mp4"  # 출력 파일 이름
merge_videos_with_filenames(folder_path, output_filename)
