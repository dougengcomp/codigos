import os
import sys
import re
import speech_recognition as sr

def recognize_speech(audio_file):
    """Performs speech recognition on the audio file.

    Takes the path to the audio file and returns the recognized text.
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)  # Read the entire audio file
    try:
        text = recognizer.recognize_google(audio_data) #,language="pt-BR" )
    except sr.UnknownValueError:
        text = "Could not understand audio"
    except sr.RequestError as e:
        text = "Could not request results; {0}".format(e)
    return text

def main(directory):
    """Process each chunk .wav file in the directory."""
    for filename in os.listdir(directory):
        if re.match(r'^chunk-\d+\.wav$', filename):
            audio_file = os.path.join(directory, filename)
            text = recognize_speech(audio_file)
            text_file = os.path.splitext(audio_file)[0] + ".txt"
            with open(text_file, 'w') as file:
                file.write(text)
            print(f"Text saved to: {text_file}")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: python text_to_speech.py <directory>\n')
        sys.exit(1)
    main(sys.argv[1])
