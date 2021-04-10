#! python3
# SES-Finder (sesf): search for a given item number in the old AutoCAD directory,
# the Vault, personal reference models and the NC program library.
#
# Third-party modules required:
#   pyinputplus

import os, sys, subprocess, pyinputplus
import logging
from time import sleep
from pathlib import Path
from pyautogui import alert

# Configuration
## logging setup
logFilePath = Path(r'C:\Users\chavesd\python_scripts\sesf\sesfLogFile.log')
## delete old log file
os.unlink(logFilePath) # comment-out if you want to see logs for more than one search.
logging.basicConfig(filename=logFilePath, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
#logging.disable() # remove comment to disable logging
logging.debug(r'(*-*) sesf started! (*-*)')

## Search locations
## These paths may need to be updated depending on the computer this is on.
## Not everyone has the `\\fap02\` public drive mapped to `P:\`
AUTOCAD     =   Path(r'P:\HPD_Shar\08 - SES ENGINEERING\Engineering')
VAULT       =   Path(r'C:\AWC_Vault\Eng Polymer Solutions\Spring Energized Seal')
NCPLIB      =   Path(r'P:\HPD_Shar\07_SES_MFG\SES PROGRAMS FOR PRODUCTION')
SLDREF      =   Path(r'C:\Users\chavesd\OneDrive - A.W.Chesterton Company\SES-solids')

## Paths to executables that will be used to open the selected file.
EDRAWINGS   =   Path(r'C:\Program Files\SOLIDWORKS Corp\eDrawings\EModelViewer.exe')
SOLIDWORKS  =   Path(r'C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SLDWORKS.exe')
EDITNC      =   Path(r'C:\Program Files (x86)\editNC11\editNC11.exe')
VIM         =   Path(r'C:\Program Files (x86)\Vim\vim82\gvim.exe')

## Misc. configs, constants
SELECT_FILE_PROMPT = "Select one of these files:\n"

# Functions
def usage():
    """Prints useage information to stdout."""
    if len(sys.argv) <= 1:
        print(
            """sesf usage:
            sesf -[p|v|c] ITEM_NUMBER"""
        )
        sleep(3)
        sys.exit(2)

def search(itemNumber, location):
    """Search for string `itemNumber` at the specified `location`.
    Returns a list of Path objects with `name` attributes that contain the string `itemNumber`.
    `location` is one of the Path objects in the *search locations* config section."""
    itemNumber = itemNumber.upper()
    prefix = getPrefix(itemNumber)
    matches = []
    if location == AUTOCAD:
        # In the `AUTOCAD` location, these "prefixes" are located in the M06 dir. 
        if prefix in ('FMD', 'FM3'):
            searchPath = Path.joinpath(AUTOCAD, 'M06')
        else:
            searchPath = Path.joinpath(AUTOCAD, prefix)
        
        logging.debug(f'Searching for {itemNumber} in {prefix}...')
        for filename in searchPath.glob('*.dwg'):
            if itemNumber in filename.name.upper():
                matches.append(Path.joinpath(searchPath, filename.name))
        return matches

    elif location == VAULT:
        logging.debug("Searching in The Vault...")
        # No subdirs to worry about in vault. Go straight to searchin'
        for filename in os.listdir(VAULT):
            if itemNumber in filename:
                matches.append(Path.joinpath(VAULT, filename))
        return matches

    elif location == NCPLIB:
        logging.debug(f"Searching in NC Program Library {prefix}...")
        searchPath = Path.joinpath(NCPLIB, prefix)
        for filename in searchPath.glob('*.nc'):
            if itemNumber in filename.name.upper():
                matches.append(Path.joinpath(searchPath, filename.name))
        return matches
    
    elif location == SLDREF:
        logging.debug(f"Searching Personal Reference Solids {prefix}...")
        searchPath = Path.joinpath(SLDREF, prefix)
        for dirs, subdirs, files in os.walk(searchPath):
            for file in files:
                if itemNumber in file:
                    matches.append(Path.joinpath(searchPath, file))
        return matches

def getPrefix(itemNumber):
    """Returns the prefix of the input drawing number.
    This function simply compares the input drawing number to a tuple of known 
    drawing prefixes. If a prefix string is found within the input string, that
    prefix string is returned."""
    prefixes = ( 'C01', 'FM3', 'FMD', 'H02', 'L05', 'M06', 'R04', 'S03' )  
    for prefix in prefixes:
        if prefix in itemNumber:
            logging.debug('Prefix is %s' %(prefix))
            return prefix

    return ''

    logging.debug('No prefix found. Bad item number?')

def getFilenames(listOfPaths):
    """Return a list of filenames from a list of Path objects."""
    filenames = []
    for filename in listOfPaths:
        filenames.append(filename.name)
    
    return filenames

def getFilePath(filename, listOfPaths):
    """Finds the given filename in a list of Path objects. Returns the Path object
    which contains the filename."""
    for path in listOfPaths:
        if filename in path.name:
            return path

def noOptions(itemNumber):
    """Runs the default operation of the program.
    Search for the input item number in every location. Print the number of results
    in each location and ask the user to select a file type (cad, solid, or nc).
    After a file type is selected, display a menu of filenames that were found.
    Launch the chosen file in the appropriate program."""
    # Search for old AutoCAD drawings
    logging.debug("Searching AutoCAD directory... ")
    print("Searching AutoCAD directory... ")
    autoCADfiles = search(itemNumber, AUTOCAD)
    filenamesCAD = getFilenames(autoCADfiles)
    logging.debug("Found %s *.dwg files." %(len(autoCADfiles)))

    # Search for SolidWorks files in The Vault
    logging.debug("Searching The Vault... ")
    print("Searching The Vault... ")
    solidWorksFiles = search(itemNumber, VAULT)
    filenamesSW = getFilenames(solidWorksFiles)
    logging.debug("Found %s SolidWorks files." %(len(solidWorksFiles)))

    # Search for NC programs in the library
    logging.debug("Searching NC Program Library... ")
    print("Searching NC Program Library... ")
    ncpFiles = search(itemNumber, NCPLIB)
    ncpFilenames = getFilenames(ncpFiles)
    logging.debug("Found %s NC programs." %(len(ncpFiles)))

    # Search for personal reference solids
    logging.debug("Searching personal reference solids...")
    print("Searching personal reference solids...")
    prsFiles = search(itemNumber, SLDREF)
    prsFilenames = getFilenames(prsFiles)
    logging.debug("Found %s personal reference solids." %(len(prsFiles)))

    # Ask user what type of files they would like to see
    response = pyinputplus.inputMenu(
        ["AutoCAD .dwg files (%s)" %(len(autoCADfiles)),
        "SolidWorks models/drawings (%s)" %(len(solidWorksFiles)),
        "NC programs (%s)" %(len(ncpFiles)),
        "Personal Reference (%s)" %(len(prsFiles))],
        prompt="Select a file type:\n", numbered=True
    )
    if "AutoCAD" in response:
        # If a match occurred, it's likely only one file, `.inputMenu()` requires at least two choices.
        # If user selected "AutoCAD" and there is only 1 file, just open that file.
        # Otherwise ask user to select a file.
        logging.debug("User selected AutoCAD.")
        numberOfFiles = len(autoCADfiles)
        if numberOfFiles > 1:
            response = pyinputplus.inputMenu(filenamesCAD, prompt=SELECT_FILE_PROMPT, numbered=True)
            filePath = getFilePath(response, autoCADfiles)
            logging.debug(f"Starting subprocess: {EDRAWINGS.name} {response}")
            subprocess.Popen([EDRAWINGS, filePath])
        elif numberOfFiles == 1:
            filePath = autoCADfiles[0]
            logging.debug(f"One match found. Starting subprocess: {EDRAWINGS.name} {filePath.name}")
            subprocess.Popen([EDRAWINGS, filePath])
        else:
            logging.debug("No AutoCAD drawings found for that item number.")
    elif "SolidWorks" in response:
        # Ask user to choose a SolidWorks model/drawing
        # Item numbers in the Vault always have a model and a drawing.
        # so the search should always return at least two matches.
        numberOfFiles = len(solidWorksFiles)
        if numberOfFiles > 0:
            response = pyinputplus.inputMenu(filenamesSW, prompt=SELECT_FILE_PROMPT, numbered=True)
            filePath = getFilePath(response, solidWorksFiles)
            exeChoice = pyinputplus.inputMenu(['SolidWorks', 'eDrawings'], prompt="Open this file with...\n", numbered=True)
            if exeChoice == "SolidWorks":
                logging.debug(f"Starting subprocess: {SOLIDWORKS.name} {response}")
                subprocess.Popen([SOLIDWORKS, filePath])
            else:
                logging.debug(f"Starting subprocess: {EDRAWINGS.name} {response}")
                subprocess.Popen([EDRAWINGS, filePath])
        else:
            logging.debug("Nothing in the Vault with that item number.")
    elif "NC" in response:
        # If a single match occurred, just open the file. Otherwise, ask the 
        # user to choose a file to open.
        numberOfFiles = len(ncpFiles)
        if numberOfFiles > 1:
            response = pyinputplus.inputMenu(ncpFilenames, prompt=SELECT_FILE_PROMPT, numbered=True)
            filePath = getFilePath(response, ncpFiles)
            logging.debug(f"Starting subprocess: {EDITNC.name} {response}")
            subprocess.Popen([EDITNC, filePath])
        elif numberOfFiles == 1:
            filePath = ncpFiles[0]
            logging.debug(f"One match found. Starting subprocess: {EDITNC.name} {filePath.name}")
            subprocess.Popen([EDITNC, filePath])
        else:
            logging.debug("No NC programs found with that item number.")
    elif "Personal" in response:
        numberOfFiles = len(prsFiles)
        if numberOfFiles > 1:
            response = pyinputplus.inputMenu(prsFilenames, prompt=SELECT_FILE_PROMPT, numbered=True)
            filePath = getFilePath(response, prsFiles)
            exeChoice = pyinputplus.inputMenu(['SolidWorks', 'eDrawings'], prompt="Open this file with...\n", numbered=True)
            if exeChoice == 'SolidWorks':
                subprocess.Popen([SOLIDWORKS, filePath])
                logging.debug(f"Staring subprocess: {exeChoice} {response}")
            else:
                subprocess.Popen([EDRAWINGS, filePath])
                logging.debug(f"Staring subprocess: {exeChoice} {response}")
        elif numberOfFiles == 1:
            filePath = os.path.abspath(prsFiles[0])
            exeChoice = pyinputplus.inputMenu(['SolidWorks', 'eDrawings'], prompt="Open this file with...\n", numbered=True)
            if exeChoice == 'SolidWorks':
                subprocess.Popen([SOLIDWORKS, filePath])
            else:
                subprocess.Popen([EDRAWINGS, filePath])
            logging.debug(f"Staring subprocess: {exeChoice} {response}")


# Main program section
numArgs = len(sys.argv)

## Test each location. Network drives or Vault may be inaccessable. If this is
## the case, inform the user and exit the program.
for location in (AUTOCAD, VAULT, NCPLIB):
    if location.exists() == False:
        logging.debug('Path does not exist: %s \nAre your network drives mounted?' %(location))
        sys.exit(1)

## parse arguments
if numArgs <= 1: # Not enough args
    usage()
    logging.debug("User didn't enter enough arguments.")
elif numArgs == 2: # Item number without an option. 
    item = sys.argv[1]
    logging.debug("Item #%s; no option args. Searching all locations." %(item))
    noOptions(item)
elif numArgs == 3: # Item number with an option.
    option, item = sys.argv[1].lower(), sys.argv[2]
    if option == '-c':
        # AutoCAD-only option
        logging.debug("Item #%s; search limited to AutoCAD location." %(item))
        autoCADfiles = search(item, AUTOCAD)
        filenames = getFilenames(autoCADfiles)
        numberOfFiles = len(filenames)
        # An AutoCAD search is more likely than not to return only 1 file. In
        # which case, `pyinputplus.inputMenu()` won't work.
        if numberOfFiles > 1:
            response = pyinputplus.inputMenu(filenames, prompt=SELECT_FILE_PROMPT, numbered=True)
            filePath = getFilePath(response, autoCADfiles)
            subprocess.Popen([EDRAWINGS, filePath])
            logging.debug(f"Launched subprocess: {EDRAWINGS.name} {filePath.name}")
        elif numberOfFiles == 1:
            filePath = getFilePath(filenames[0], autoCADfiles)
            subprocess.Popen([EDRAWINGS, filePath])
            logging.debug(f"Launched subprocess: {EDRAWINGS.name} {filePath.name}")
        else:
            logging.debug("Didn't find anything with that item number.")
    elif option == '-v':
        # SolidWorks Vault-only option
        # The Vault should contain at least two files for every item number (model, drawing).
        # So, if there is a match for the item number, it will match at least two files.
        logging.debug("Item #%s; search limited to The Vault." %(item))
        solidWorksFiles = search(item, VAULT) # returns a list of Path objects
        if len(solidWorksFiles) == 0:
            logging.debug(
                """Didn't find anything in The Vault with that item number.
                Try updating the `Spring Engergized Seal` directory to make sure you have the latest files and try again.
                Go to *C:\AWC_Vault\eng polymer solutions*, right click the SES dir and select 'Get latest version'."""
                )
        else:
            logging.debug("Found %s files." %(len(solidWorksFiles)))
            filenames = getFilenames(solidWorksFiles)
            fileChoice = pyinputplus.inputMenu(filenames, prompt=SELECT_FILE_PROMPT, numbered=True)
            filePath = getFilePath(fileChoice,solidWorksFiles)
            exeChoice = pyinputplus.inputMenu(['SolidWorks', 'eDrawings'], prompt="Open this file with...\n", numbered=True)
            # The vault contains solid models and drawings, either of which can be opened in
            # SolidWorks or eDrawings viewer. Ask the user what they want.
            if exeChoice == 'SolidWorks':
                subprocess.Popen([SOLIDWORKS, filePath])
                logging.debug(f"Launched subprocess: {SOLIDWORKS.name} {fileChoice}")
            else:
                subprocess.Popen([EDRAWINGS, filePath])
                logging.debug(f"Launched subprocess: {EDRAWINGS.name} {fileChoice}")
    elif option == '-p':
        # NC program-only option
        logging.debug("Item #%s; search limited to NC Program Library." %(item))
        ncpFiles = search(item, NCPLIB) # returns a list of Path objects.
        filenames = getFilenames(ncpFiles)
        numberOfFiles = len(filenames)
        # In the event a search only returns one file, `pyinputplus.inputMenu()`
        # won't work, so just go ahead and open the file.
        if numberOfFiles > 1:
            response = pyinputplus.inputMenu(filenames, prompt="Choose a file...\n", numbered=True)
            filePath = getFilePath(response, ncpFiles)
            subprocess.Popen([EDITNC, filePath])
            logging.debug(f"Launched subprocess: {EDITNC.name} {filePath.name}")
        elif numberOfFiles == 1:
            logging.debug("Item: %s - Found one file." %(item))
            filePath = getFilePath(filenames[0], ncpFiles)
            subprocess.Popen([EDITNC, filePath])
            logging.debug(f"Launched subprocess: {EDITNC.name} {filePath.name}")
        else:
            logging.debug("Didn't find any NC programs with that item number." %(item))
            alert(text="Didn't find any NC programs for that item number.", title="No matches")
    else:
        logging.debug("Unrecognized option: %s" %(option))
elif numArgs > 3: # Too many args
    usage()
    logging.debug("User entered too many arguments.")
else:
    logging.debug("This should have never happened. Something went very wrong.")