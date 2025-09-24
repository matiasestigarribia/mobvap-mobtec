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
        temp_path = temp_f.name

    thumbnail_path = generate_thumbnail(temp_path)

    # This part is also correct and doesn't need to change
    thumbnail_file = None
    if thumbnail_path and os.path.exists(thumbnail_path):
        thumbnail_file = File(
            open(thumbnail_path, 'rb'),
            name=os.path.splitext(os.path.basename(uploaded_file.name))[0] + '.jpeg'
        )
    uploaded_file.seek(0)

    # Clean up the temporary files
    os.remove(temp_path)
    if thumbnail_path and os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
        
    return uploaded_file, thumbnail_file


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
