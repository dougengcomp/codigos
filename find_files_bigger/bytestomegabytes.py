def bytes_to_megabytes(bytes_size):
    return bytes_size / (1024 * 1024)

def convert_to_megabytes(logfile, output_logfile):
    with open(logfile, 'r') as f:
        with open(output_logfile, 'w') as out_file:
            lines = f.readlines()
            for line in lines:
                parts = line.split(',')
                file_path = parts[0].split(':', 1)[1].strip()  # Preserve whole path and filename
                size_bytes = int(parts[1].split(':')[1].split()[0].strip())
                size_mb = bytes_to_megabytes(size_bytes)
                out_file.write(f"File: {file_path}, Size: {size_mb:.2f} MB\n")

def main():
    logfile = 'large_files_log.txt'
    output_logfile = 'large_files_log_megabytes.txt'
    convert_to_megabytes(logfile, output_logfile)
    print(f"Converted sizes saved to {output_logfile}")

if __name__ == "__main__":
    main()
