with open(r"C:\Users\rijul\codigos\testesimples\textfile.txt", "r", encoding="cp1252") as myfile:
    # Read the contents of the file
    file_contents = myfile.read()
    # Print the contents to the console
    print(file_contents)
    myfile.seek(0)
    file_contents = myfile.read()
    print(file_contents)