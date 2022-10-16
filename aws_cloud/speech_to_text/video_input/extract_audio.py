import sys
from moviepy.editor import AudioFileClip, VideoFileClip
import argparse
from pathlib import PurePath
import os


VIDEO_PATH = r"C:\Users\Mehmet\PycharmProjects\textTospeech\voice_recognition\aws_cloud\speech_to_text\videos"
EXTRACTED_AUDIO_PATH = r"C:\Users\Mehmet\PycharmProjects\textTospeech\voice_recognition\aws_cloud\speech_to_text\extracted_audios"


def extract_audio(input_file, output_path):
    """
    Extracts audio from a given video file
    :param input_file:
    :param output_path:
    :return:
    """
    path = PurePath(input_file)
    out_file = output_path + f"\\{path.stem}" + ".mp3"
    try:
        print("Extracting process has started... Please wait...")
        video = VideoFileClip(input_file)
        audio = video.audio
        # audio = AudioFileClip(input_file)
        audio.write_audiofile(out_file)
    except Exception as exception:
        print("Unknown error occured. Exiting.")
        print(exception)
        sys.exit(-1)
    print("Succesfull.")


def extract_audios(input_folder_path, output_path):
    videos = []
    for root, dirs, files in os.walk(input_folder_path):
        for name in files:
            video_file = os.path.join(root, name)
            videos.append(video_file)
    for file in videos:
        extract_audio(file, output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="usage: python extract_audio.py")
    parser.add_argument('--inputPath', default=VIDEO_PATH, type=str)
    parser.add_argument('--outputPath', default=EXTRACTED_AUDIO_PATH, type=str)
    args = parser.parse_args()

    if args.inputPath:
        if os.path.isfile(args.inputPath):
            extract_audio(args.inputPath, args.outputPath)
            sys.exit()

        else:
            extract_audios(args.inputPath, args.outputPath)




