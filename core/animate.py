import subprocess
import numpy as np
from constants import FFMPEG_BIN
from constants import VIDEO_FRAME_RATE

class animate:
    def __init__(self, width, height, video_name, frame_rate = VIDEO_FRAME_RATE):
        self._width = width
        self._height = height
        self._name = video_name
        self._frame_rate = frame_rate

    def open_writing_pipeline(self):
        command = [
            FFMPEG_BIN,
            "-y",  # override
            "-f", "rawvideo",
            "-s", "%dx%d" % (self._width, self._height),
            "-pix_fmt", "rgba",
            "-r", '%d' % self._frame_rate,
            "-i", "-",
            "-an",
            "-loglevel", "error",
            "-vcodec",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            self._name,
        ]

        self._writing_pipeline = subprocess.Popen(command, stdin=subprocess.PIPE)

    def write_frame(self, frame_array):
        self._writing_pipeline.stdin.write(frame_array.tostring())

    def close_writing_pipeline(self):
        self._writing_pipeline.stdin.close()
        self._writing_pipeline.wait()
