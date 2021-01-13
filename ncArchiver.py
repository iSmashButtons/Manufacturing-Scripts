#! python3
#     ____  _____ ______
#    / __ \/ ___// ____/	script by Dennis Chaves
#   / / / /\__ \/ /    		github.com/ismashbuttons 
#  / /_/ /___/ / /___  		dennis@dennischaves.xyz
# /_____//____/\____/   
#                       
# ncArchiver
# creates an archive of the "SES PROGRAM LIBRARY" folder.

import os, zipfile
from pathlib import Path
from datetime import date

# Today's date
today = date.today()
year, month, day = str(today.year), str(today.month), str(today.day) 

os.chdir(r'P:\HPD_Shar\07_SES_MFG')
seslib = Path(r'SES PROGRAMS FOR PRODUCTION')
archivePath = Path(r'P:\HPD_Shar\07_SES_MFG\ncArchive') / year # Where the zip file will end up
archiveName = month + '-' + day + '.zip'

# Create archive path
os.makedirs(archivePath, exist_ok=True)

# Create the zipfile
print(f'Creating archive: {archiveName}...')
archive = zipfile.ZipFile(archivePath / archiveName, 'w')

# Walk through program library
for root, dirs, files in os.walk(seslib):
    # add the current root dir to the archive
    print(f'Archiving dir: {root}')
    archive.write(root)

    # add all the files in root dir to archive
    for filename in files:
        print(f'Archiving program: {filename}...')
        archive.write(os.path.join(root, filename), compress_type=zipfile.ZIP_DEFLATED)

archive.close()

print('Archive complete. Happy Friday!')
