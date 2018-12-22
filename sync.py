from sys import argv
from os  import scandir
from os import path
from os import remove
from pathlib import Path
from shutil import copyfile

source: str = '/Volumes/Passport/comics/on-deck'
# target: str = '/Volumes/Public/webbox'
target: str = '/Volumes/Passport/tmp-ondeck'

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
        return string[prefix_length:]

def isArchiveDir(directory):
    return not 'yacreader' in directory

def filterArchives(archive):
    isArchive:bool =  (archive.endswith('.cbz') or archive.endswith('.cbr'))
    yacreader:bool = '.yacreader' in archive
    isHidden:bool = path.basename(archive).startswith('.') or path.basename(archive).startswith('_')
    return isArchive and not yacreader and not isHidden


def diffLists(list1, list2):
    diff = [aa for aa in list1 if aa not in list2]
    return diff

def insert(file):
    source_archive: str = source + file
    target_archive: str = target + file

    #Generate the parent directory, if missing
    Path(target_archive).parent.mkdir(parents=True, exist_ok=True);

    #Copy...
    print('-- > ', file)
    copyfile(source_archive, target_archive)
    print('.. copied')

def remove(file):
    target_archive: str = target + file

    print('< -- ', target_archive)
    remove(target_archive)
    print('.. removed.')


source_files = scan(source)
source_files = list(filter(filterArchives, source_files))
source_relative = [chompLeft(p, source) for p in source_files]

target_files = scan(target)
target_files = list(filter(filterArchives, target_files))
target_relative = [chompLeft(p, target) for p in target_files]

print( len(source_files), ' source files scanned, ', len(target_files), ' target files scanned.')


inserts = diffLists(source_relative, target_relative)
deletes = diffLists(target_relative, source_relative)

print('Removing ', len(deletes))
for datum in deletes:
    remove(datum)

print('Copying ', len(deletes))
for datum in inserts:
    insert(datum)

print( 'Done!')




