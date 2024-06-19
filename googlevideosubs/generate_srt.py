def generate_srt(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    subtitles = []
    index = 1
    for line in lines:
        if line.startswith("Word:"):
            parts = line.strip().split(', ')
            word = parts[0].split(': ')[1]
            start_time = float(parts[1].split(': ')[1])
            end_time = float(parts[2].split(': ')[1])
            subtitle = {
                'index': index,
                'start_time': start_time,
                'end_time': end_time,
                'word': word
            }
            subtitles.append(subtitle)
            index += 1

    with open(output_file, 'w') as f:
        for subtitle in subtitles:
            f.write(f"{subtitle['index']}\n")
            f.write(f"{format_timestamp(subtitle['start_time'])} --> {format_timestamp(subtitle['end_time'])}\n")
            f.write(f"{subtitle['word']}\n\n")

def format_timestamp(timestamp):
    milliseconds = int((timestamp - int(timestamp)) * 1000)
    hours = int(timestamp / 3600)
    minutes = int((timestamp % 3600) / 60)
    seconds = int(timestamp % 60)
    timestamp_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    return f"{timestamp_str},{milliseconds:03d}"

# Example usage
input_file = "transcription.txt"
output_file = "output.srt"
generate_srt(input_file, output_file)
