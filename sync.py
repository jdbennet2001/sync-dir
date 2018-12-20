from sys import argv
from os  import scandir
from os import path

source: str = '/Volumes/Passport/comics'
target: str = '/Volumes/Public/webbox'

print( 'Mapping ' , source,  ' to ' , target )

def scan(directory):

    files = []

    for entry in scandir(directory):
        if entry.is_dir():
            dir:str = entry.path
            print('.. scanning.. ', dir)
            if ( isArchiveDir(dir) ):
                files += scan(dir)

        if entry.is_file():
            files.append(entry.path)

    return files

def chompLeft(string, prefix):
    if string.startswith(prefix):
        prefix_length: int = len(prefix)
        return prefix_length[prefix_length:]

def isArchiveDir(directory):
    return not 'yacreader' in directory

def filterArchives(archive):
    isArchive:bool =  (archive.endswith('.cbz') or archive.endswith('.cbr'))
    yacreader:bool = '.yacreader' in archive
    isHidden:bool = path.basename(archive).startswith('.') or path.basename(archive).startswith('_')
    return isArchive and not yacreader and not isHidden

source_files = scan(source)
source_files = list(filter(filterArchives, source_files))

for file in source_files:
    print('...', file)

print( len(source_files), 'files scanned.')

target_files = scan(target)
target_files = list(filter(filterArchives, target_files))

for file in target_files:
    print('...', file)

print( len(source_files), ' source files scanned, ', len(target_files), ' target files scanned.')




# print( sys.argv )