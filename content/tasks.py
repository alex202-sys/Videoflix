import subprocess
import os


def convert_480p(source_file_path):
    """
    Converts the given video file to 480p resolution using ffmpeg.
    """
    target = source_file_path + "480p.mp4"
    cmd = 'ffmpeg -i "{}" -vf scale=-1:480 -vcodec mpeg4 -qscale 3 "{}"'.format(
        source_file_path, target
    )
    subprocess.run(cmd, shell=True, check=True)
