def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    return content

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
    return True

def search_in_file(file_path, search_term):
    with open(file_path, 'r') as file:
        content = file.read()
    return search_term in content