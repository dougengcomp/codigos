from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech
import io
import os
import moviepy.editor as mp

def convert_to_mono(audio_file):
    sound = AudioSegment.from_wav(audio_file)
    sound = sound.set_channels(1)
    sound.export(audio_file, format="wav")

def get_audio_sample_rate(audio_file):
    audio = AudioSegment.from_file(audio_file)
    return audio.frame_rate

def transcribe_video_segments(video_file, output_file, segment_duration_seconds=10):
    client = speech.SpeechClient()

    # Extract audio from the video file
    video_audio = mp.AudioFileClip(video_file)
    video_audio.write_audiofile("temp_audio.wav", codec='pcm_s16le')

    # Convert audio to mono
    convert_to_mono("temp_audio.wav")

    # Get total duration of the video
    video_duration = video_audio.duration

    # Define the segment duration in seconds
    segment_duration = segment_duration_seconds

    # Calculate the number of segments needed
    num_segments = int(video_duration / segment_duration) + 1

    # List to store transcription results
    transcription_results = []

    # Transcribe each segment separately
    for i in range(num_segments):
        print(f"Current iteration: {i}")
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, video_duration)

        # Extract segment of audio
        audio = AudioSegment.from_wav("temp_audio.wav")[int(start_time * 1000):int(end_time * 1000)]
        audio.export(f"segment_{i}.wav", format="wav")

        # Read the audio file
        sample_rate = get_audio_sample_rate(f"segment_{i}.wav")

        # Read the audio file
        with io.open(f"segment_{i}.wav", "rb") as audio_content:
            audio_content = audio_content.read()

        # Configure the transcription request
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=sample_rate,
            language_code="en-US",  
            enable_word_time_offsets=True,
            enable_speaker_diarization=False,
        )

        # Perform the transcription request
        audio = speech.RecognitionAudio(content=audio_content)
        response = client.recognize(request={"config": config, "audio": audio})

        # Store transcription results for this segment
        segment_transcription = ""
        for result in response.results:
            for word_info in result.alternatives[0].words:
                # Adjust word start and end times for the segment
                start_time = word_info.start_time.total_seconds() + (i * segment_duration)
                end_time = word_info.end_time.total_seconds() + (i * segment_duration)
                word = word_info.word
                segment_transcription += f"Word: {word}, Start Time: {start_time}, End Time: {end_time}\n"

        transcription_results.append(segment_transcription)

        # Delete the temporary audio file
        os.remove(f"segment_{i}.wav")

    # Write transcription results to the output file
    with open(output_file, 'w') as f_out:
        for transcription in transcription_results:
            f_out.write(transcription)

    # Delete the temporary audio file
    os.remove("temp_audio.wav")

# Example usage
video_file = "file.mp4"
output_file = "transcription.txt"
transcribe_video_segments(video_file, output_file)
