import os

def read_timestamp_file(timestamp_file):
    timestamps = []
    with open(timestamp_file, 'r') as file:
        start_time = None
        for line in file:
            if line.startswith("Start Time:"):
                start_time = float(line.split(":")[1])
            elif line.startswith("End Time:"):
                end_time = float(line.split(":")[1])
                timestamps.append((start_time, end_time))
                start_time = None
    return timestamps

def generate_srt(timestamp_files_folder, output_srt_file):
    srt_content = ""
    timestamp_files = [f for f in os.listdir(timestamp_files_folder) if f.startswith("timestamp-")]
    timestamp_files.sort()
    index = 1

    for timestamp_file in timestamp_files:
        timestamp_path = os.path.join(timestamp_files_folder, timestamp_file)
        text_path = os.path.join(timestamp_files_folder, "chunk-" + timestamp_file.split("-")[1].split(".")[0] + ".txt")
        timestamps = read_timestamp_file(timestamp_path)
        with open(text_path, 'r') as text_file:
            text_content = text_file.read()
        for start, end in timestamps:
            srt_content += f"{index}\n"
            srt_content += format_time(start) + " --> " + format_time(end) + "\n"
            srt_content += f"{text_content}\n\n"
            index += 1
    
    with open(output_srt_file, 'w') as srt_file:
        srt_file.write(srt_content)

def format_time(time_in_seconds):
    """Formats time from seconds to hh:mm:ss,mls format."""
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

if __name__ == "__main__":
    timestamp_files_folder = "."
    output_srt_file = "your_audio_file.srt"
    generate_srt(timestamp_files_folder, output_srt_file)
