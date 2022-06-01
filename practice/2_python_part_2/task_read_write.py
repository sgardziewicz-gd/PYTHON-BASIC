"""
Read files from ./files and extract values from them.
Write one file with all values separated by commas.

Example:
    Input:

    file_1.txt (content: "23")
    file_2.txt (content: "78")
    file_3.txt (content: "3")

    Output:

    result.txt(content: "23, 78, 3")
"""
import os

path_to_files = "practice/2_python_part_2/files"
files = os.listdir(path_to_files)
values = []

for file in sorted(files, key=lambda x: int(os.path.splitext(x)[0][5:])):
    with open(os.path.join(path_to_files, file), 'r') as f:
        for line in f:
            values.append(line.rstrip())
            

with open("practice/2_python_part_2/result.txt", 'w') as f:
    f.write(', '.join(values))
