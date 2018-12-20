from sys import argv
from os  import scandir

source: str = '/Volumes/Passport/comics'
target: str = '/Volumes/Public/webbox'

print( 'Mapping ' , source,  ' to ' , target )

def scan(directory):

    files = []

    for entry in scandir(directory):
        if entry.is_dir():
            dir:str = entry.path
            print('.. scanning.. ', dir)
            files += scan(dir)

        if entry.is_file():
            files.append(entry.path)

    return files


source_files = scan(source)
target_files = scan(target)

print( len(source_files), ' source files scanned, ', len(target), ' target files scanned.')




# print( sys.argv )