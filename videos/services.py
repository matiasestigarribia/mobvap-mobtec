import ffmpeg
import os
import tempfile
from django.core.files import File


import ffmpeg
import os
import tempfile
from django.core.files import File

def process_video(uploaded_file):
    # This part is correct and doesn't need to change
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_f:
        for chunk in uploaded_file.chunks():
            temp_f.write(chunk)
        initial_temp_path = temp_f.name

    # Run your updated conversion and compression steps
    converted_path = convert_to_mp4(initial_temp_path)
    compressed_path = compress_video(converted_path)
    thumbnail_path = generate_thumbnail(compressed_path)

    # This part is also correct and doesn't need to change
    thumbnail_file = None
    if thumbnail_path and os.path.exists(thumbnail_path):
        thumbnail_file = File(
            open(thumbnail_path, 'rb'),
            name=os.path.splitext(os.path.basename(uploaded_file.name))[0] + '.jpeg'
        )
    processed_video_file = File(open(compressed_path, 'rb'), name=os.path.splitext(os.path.basename(uploaded_file.name))[0] + '.mp4')

    # Clean up the temporary files
    os.remove(initial_temp_path)
    if converted_path and converted_path != initial_temp_path:
        os.remove(converted_path)
    if compressed_path and compressed_path != converted_path:
        os.remove(compressed_path)
    if thumbnail_path and os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)

    return processed_video_file, thumbnail_file


def convert_to_mp4(input_path):
    root, ext = os.path.splitext(input_path)
    if ext.lower() == '.mp4':
        return input_path

    output_path = root + '_converted.mp4'
    try:
        (
            ffmpeg
            .input(input_path)
            .output(output_path)
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output_path
    except ffmpeg.Error as e:
        print(f"Error converting video: {e.stderr.decode()}")
        return input_path


def compress_video(input_path):
    root, ext = os.path.splitext(input_path)
    output_path = root + '_compressed.mp4'
    try:
        (
            ffmpeg
            .input(input_path)
            # This smarter filter scales the video to a max width of 1280
            # while preserving the original aspect ratio.
            .filter('scale', 1280, -1)
            .output(output_path, **{'crf': '23'})
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output_path
    except ffmpeg.Error as e:
        print(f"Error compressing video: {e.stderr.decode()}")
        return input_path


def generate_thumbnail(input_path):
    output_path = os.path.splitext(input_path)[0] + '.jpeg'
    try:
        (
            ffmpeg
            .input(input_path, ss='00:00:05')
            # No more filters! Just grab the frame.
            .output(output_path, vframes=1)
            .run(capture_stdout=True, capture_stderr=True)
        )
        return output_path
    except ffmpeg.Error as e:
        print(f"Error generating thumbnail: {e.stderr.decode()}")
        return None