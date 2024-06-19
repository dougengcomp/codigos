def timestamp_to_seconds(timestamp):
    h, m, s = map(float, timestamp.split(':'))
    return 3600 * h + 60 * m + s

def parse_timestamp(timestamp):
    parts = timestamp.split(' --> ')
    start = timestamp_to_seconds(parts[0].replace(',', '.'))
    end = timestamp_to_seconds(parts[1].replace(',', '.'))
    return start, end

def format_timestamp(seconds):
    hours = int(seconds // 3600)
    seconds %= 3600
    minutes = int(seconds // 60)
    seconds %= 60
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"

def break_subtitle(subtitle):
    lines = subtitle.split('\n')
    timestamp = lines[1]
    start, end = parse_timestamp(timestamp)
    duration = end - start
    text = '\n'.join(lines[2:])
    chunks = []
    if duration > 3:
        num_chunks = int(duration / 3) + 1
        chunk_duration = duration / num_chunks
        words = text.split()
        chunk_texts = [' '.join(words[i:i+10]) for i in range(0, len(words), 10)]  # Split text into chunks of 10 words
        for i, chunk_text in enumerate(chunk_texts):
            chunk_start = start + i * chunk_duration
            chunk_end = min(start + (i + 1) * chunk_duration, end)
            chunk_lines = [str(i + 1), f"{format_timestamp(chunk_start)} --> {format_timestamp(chunk_end)}", chunk_text]  # Adjust timestamp format
            chunks.append('\n'.join(chunk_lines))
    else:
        chunks.append(subtitle)
    return chunks

def process_srt(input_file, output_file):
    with open(input_file, 'r') as f:
        subtitles = f.read().strip().split('\n\n')
    
    output_subtitles = []
    index = 1  # Initialize subtitle index
    for subtitle in subtitles:
        subtitle_chunks = break_subtitle(subtitle)
        for chunk in subtitle_chunks:
            if '-->' in chunk:  # If the chunk contains a timestamp
                output_lines = chunk.split('\n')
                output_lines[0] = str(index)  # Update the subtitle index
                chunk = '\n'.join(output_lines)
                index += 1  # Increment index for the next subtitle
            output_subtitles.append(chunk)
    
    with open(output_file, 'w') as f:
        f.write('\n\n'.join(output_subtitles))

# Example usage
input_file = "your_audio_file.srt"
output_file = "output.srt"
process_srt(input_file, output_file)
