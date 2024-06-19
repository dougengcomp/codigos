from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def timestamp_to_seconds(timestamp):
    # Split the timestamp string into start and end timestamps
    start, end = timestamp.split(" --> ")

    # Split each timestamp at ':', and further at ','
    start_h, start_m, start_s_ms = start.split(":")
    end_h, end_m, end_s_ms = end.split(":")
    
    # Split seconds and milliseconds
    start_s, start_ms = start_s_ms.split(",")
    end_s, end_ms = end_s_ms.split(",")

    # Convert all parts to seconds
    start_seconds = float(start_h) * 3600 + float(start_m) * 60 + float(start_s) + float(start_ms) / 1000
    end_seconds = float(end_h) * 3600 + float(end_m) * 60 + float(end_s) + float(end_ms) / 1000

    return start_seconds, end_seconds

def add_subtitles(video_path, subtitles_path, output_path, bitrate="1k", resolution=None, frame_rate=None):  
    # Load the video clip
    video_clip = VideoFileClip(video_path)
    
    # Reduce resolution if specified
    if resolution:
        video_clip = video_clip.resize(resolution)

    # Adjust frame rate if specified
    if frame_rate:
        video_clip = video_clip.set_fps(frame_rate)

    # Open subtitles file and read lines
    try:
        with open(subtitles_path, 'r', encoding='utf-8') as file:
            subtitle_lines = file.readlines()
    except UnicodeDecodeError:
        with open(subtitles_path, 'r', encoding='latin-1') as file:  
            subtitle_lines = file.readlines()

    # Process subtitle lines
    subtitles = []
    for i in range(0, len(subtitle_lines), 4):
        # Extract timestamp and text
        timestamp = subtitle_lines[i+1].strip()
        start_time, end_time = timestamp_to_seconds(timestamp)
        text = subtitle_lines[i+2].strip()

        # Append to subtitles list
        subtitles.append((start_time, end_time, text))

    # Generate text clips for subtitles
    text_clips = []
    for start_time, end_time, subtitle_text in subtitles:
        text_clip = TextClip(subtitle_text, fontsize=48, color='yellow', bg_color='black', font='Arial-Bold')  # Changed fontsize, color, and bg_color
        text_clip = text_clip.set_start(start_time).set_end(end_time).set_position(('center', 'bottom'))  # Centered and placed at the bottom
        text_clips.append(text_clip)

    # Composite video clip with subtitles
    final_clip = CompositeVideoClip([video_clip] + text_clips)

    # Write the subtitled video file with specified bitrate
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", temp_audiofile="temp-audio.m4a", remove_temp=True, bitrate=bitrate)

# Example usage
video_path = "my_original_video_file.mp4"
subtitles_path = "your_audio_file.srt"
output_path = "my_subtitled_video_file.mp4"
add_subtitles(video_path, subtitles_path, output_path, bitrate="20280k",  frame_rate=29)  # Set resolution and frame rate as needed
