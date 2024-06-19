from moviepy.editor import VideoFileClip

def extract_audio(input_video, output_audio, framerate=32000, codec="pcm_s16le"):
    # Load the video clip
    video_clip = VideoFileClip(input_video)
    
    # Extract audio
    audio_clip = video_clip.audio
    
    # Resample audio to the desired frame rate
    audio_clip = audio_clip.set_fps(framerate)
    
    # Save the audio with mono channel configuration
    audio_clip.write_audiofile(output_audio, codec=codec, ffmpeg_params=['-ac', '1'])

    # Close the video clip
    video_clip.close()

# Example usage
input_video = "my_original_video_file.mp4"
output_audio = "output_audio.wav"
extract_audio(input_video, output_audio)
