import os.path as path

def output_file(file):
    parent_dir = path.dirname(path.dirname(path.dirname(__file__)))
    output_dir = path.join(path.join(parent_dir,"output"),file)
    return output_dir