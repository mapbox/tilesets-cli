import os

def absoluteFilePaths(directory):
    for dirpath,_,filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))

def flatten(files):
    for f in files:
        if os.path.isdir(f):
            for dir_file in absoluteFilePaths(f):
                yield dir_file
        else:
            yield f
