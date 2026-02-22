import ffmpeg
import numpy as np
import io

async def framer(file_bytes):
    process = (
        ffmpeg.video
    )