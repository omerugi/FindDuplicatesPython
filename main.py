import os
from pathlib import Path
import hashlib

# Iterate over each path to extract the files
# Return a dict tha contain only the file with duplicates
# Key = MD5 on the file, Value = Set of all the path's to the same file
def findDuplicate(path_arr:list):
    duplic = {}
    for dir_path in path_arr:
        joinDict(duplic, iterOverDirectory(dir_path))
    return {k: v for k, v in duplic.items() if len(v) > 1}

# Joining together dict's that return from different path's
def joinDict(dict1, dict2):
    for key in dict2:
        if key in dict1:
            dict1[key] = dict1[key].union(dict2[key])
        else:
            dict1[key] = dict2[key]

# Iterate over a directory from top to bottom
# Hashing each file and keeping it in a dict
def iterOverDirectory(dir_path):
    dup = {}
    folders = Path(dir_path)
    for (root, dirs, files) in os.walk(folders, topdown=True):
        for f in files:
            path = os.path.join(root, f)
            file_hash = hashFile(path)
            if file_hash not in dup:
                dup[file_hash] = set()
            dup[file_hash].add(path)
    return dup

# Hasing a file using MD5
# Open, read and then iterate over the bits in "blocksize"
def hashFile(path):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    blocksize = 65536
    buf = afile.read(blocksize)

    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()



