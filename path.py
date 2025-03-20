import os

def find_generated_path(path):
    if os.path.isfile(path):
        # If the path is a file, find the corresponding generated file path
        file_name, file_extension = os.path.splitext(path)
        if file_extension in ['.txt', '.pdf', '.md']:
            # If the file is a raw file, find the corresponding generated file path
            generated_path = path.replace('rawFile', 'embeddedVector').replace(file_extension, '.json')
            return generated_path
        elif file_extension == '.json':
            # If the file is a generated file, return the current path
            return path
    elif os.path.isdir(path):
        # If the path is a folder, find the corresponding generated folder path
        if 'rawFile' in path:
            # If the folder is a raw file folder, find the corresponding generated folder path
            generated_path = path.replace('rawFile', 'embeddedVector')
            return generated_path
        elif 'embeddedVector' in path:
            # If the folder is a generated file folder, return the current path
            return path
    return None

if __name__ == '__main__':
    path = 'database/rawFile/Git Tutorial_1.md'
    generated_path = find_generated_path(path)
    print(generated_path)