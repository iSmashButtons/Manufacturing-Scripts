import pyinputplus as pyip
import os
import psutil
from subprocess import Popen
import pyperclip
from sys import exit as buhbye
from time import sleep
from pathlib import Path
from config import *

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('*' * 25)
    print('*' + 'SES Finder'.center(23) + '*')
    print('*' + 'Version 3.0'.center(23) + '*')
    print('*' * 25)
    print()

def display_message(msg):
    print(msg)
    sleep(MSG_DELAY)

def get_item_number():
    i = pyip.inputStr(MESSAGES['itemno'])
    if i.lower() == 'q':
        buhbye()
    return i

def get_search_location():
    print(MESSAGES['where_search'])
    print('-' * len(MESSAGES['where_search']))
    selection = pyip.inputMenu(SEARCH_OPTIONS, numbered=True)
    return selection

def search(itemNumber: str, location: Path, filetype: str) -> Path:
    """Look for an item number with specific filetype at location.
    Returns a list of Path objects or an empty list if no matches are found."""
    print('Searching %s...' %(str(location)))
    itemNumber = itemNumber.upper()
    matches = []
    for dirpath, dirnames, filenames in os.walk(location):
        for name in filenames:
            if itemNumber in name:
                file_path = Path(dirpath, name)
                matches.append(file_path)

    return matches

def get_prefix(itemNumber):
    for prefix in PREFIXES:
        if prefix in itemNumber:
            return prefix
    
    display_message(f'No prefix found (item #: {itemNumber}). You probably input a badly formatted item number.')
    return ''

def get_cad_results(item_number):
    p = get_prefix(item_number)
    sl = Path.joinpath(SEARCH_LOCATIONS['cad'], p)
    r = search(item_number, sl, FILETYPES['ncprog'])
    return r

# In the future you may want to include `.ppf` files in the results. If that 
# becomes the case, remove this function and use regular `search()` instead over in `main.py`
def get_ecam_results(item_number):
    no_ppf_results = results = search(item_number, SEARCH_LOCATIONS['edgecam'], FILETYPES['anyft'])
    if len(results) > 0:
        for index, path in enumerate(results):
            if '.ppf' in path.name.lower():
                no_ppf_results.remove(no_ppf_results[index])
    return no_ppf_results

def results_by_location_menu(item, cad, vault, pref, nc, ecam):
    results_by_location = [
        "CAD                (%s)" %(len(cad)),
        "Vault              (%s)" %(len(vault)),
        "Personal Reference (%s)" %(len(pref)),
        "NC Progs           (%s)" %(len(nc)),
        "EdgeCAM Files      (%s)" %(len(ecam)),
        "Quit"
    ]
    clear_screen()
    results_msg = f'Search results for item #: {item}'
    print(results_msg)
    print('-' * len(results_msg))
    selection = pyip.inputMenu(results_by_location, numbered=True)
    return selection

def get_filenames(paths):
    filenames = []
    for path in paths:
        filenames.append(path.name)
    return filenames

def process_running(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;

def select_file_launch_exe(paths):
    '''
    Get final file selection from user and launch the appropriate executable.
    Executable is determined by file extension. File path will also be copied to
    the clipboard in case there is a failure to launch the program.
    '''
    clear_screen()
    files = get_filenames(paths)
    files.append('Quit')
    selection = pyip.inputMenu(files, numbered=True)

    # find the matching path
    for path in paths:
        if selection  in path.name:
            file_path = path
            pyperclip.copy(str(file_path))

    # start exe based on file extension
    if (selection.lower().endswith('.sldprt')
            or selection.lower().endswith('.slddrw')
            or selection.lower().endswith('.sldasm')
        ): # open in eDrawings only if solidworks is already running
        if process_running('solidworks'):
            Popen([EXECUTABLES['edrawings'], file_path])
            print("SolidWorks is already running.\nOpening eDrawings instead...")
            sleep(3)
        else:
            Popen([EXECUTABLES['solidworks'], file_path])
            print("Opening SolidWorks...")
            sleep(3)
    elif selection.lower().endswith('.nc'): # open with CIMCO Edit
        Popen([EXECUTABLES['cimco'], file_path])
        print("Opening CIMCO Edit...")
        sleep(3)
    elif selection.lower().endswith('.dwg'): # open with eDrawings
        Popen([EXECUTABLES['edrawings'], file_path])
        print("Opening eDrawings...")
        sleep(3)