import os

def find_large_files(directory, min_size):
    large_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                if file_size > min_size:
                    large_files.append((file_path, file_size))
    return large_files

def save_to_logfile(large_files, logfile):
    with open(logfile, 'w') as f:
        for file_path, size in large_files:
            f.write(f"File: {file_path}, Size: {size} bytes\n")

def main():
    directory = 'C:\\'
    min_size = 200 * 1024 * 1024  # 200 MB in bytes
    logfile = 'large_files_log.txt'
    
    large_files = find_large_files(directory, min_size)
    if large_files:
        print("Large files found:")
        for file_path, size in large_files:
            print(f"File: {file_path}, Size: {size} bytes")
        save_to_logfile(large_files, logfile)
        print(f"List of large files saved to {logfile}")
    else:
        print("No large files found.")

if __name__ == "__main__":
    main()
