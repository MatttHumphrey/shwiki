from os import path

def output_file(file):
    '''Creates the path to a file in the output folder from a script in the scripts folder.'''
    parent_dir = path.dirname(path.dirname(path.dirname(__file__)))
    output_dir = path.join(path.join(parent_dir,"output"),file)
    return output_dir
