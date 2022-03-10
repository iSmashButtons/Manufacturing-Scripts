from pathlib import Path

PREFIXES = ( 'C01', 'FM3', 'FMD', 'H02', 'L05', 'M06', 'R04', 'S03' )  

SEARCH_LOCATIONS = {
    "cad"       :   Path(r"P:\HPD_Shar\08 - SES ENGINEERING\Engineering"),
    "awc_vault" :   Path(r"C:\AWC_Vault\Eng Polymer Solutions\Spring Energized Seal"),
    "nc_lib"    :   Path(r"P:\HPD_Shar\07_SES_MFG\SES PROGRAMS FOR PRODUCTION"),
    "sld_ref"   :   Path(r"C:\Users\chavesd\OneDrive - A.W.Chesterton Company\SES-solids"),
    "edgecam"   :   Path(r"P:\HPD_Shar\07_SES_MFG\Edgecam Files")
}

FILETYPES = {
    "sldprt" : '*.SLDPRT',
    "slddrw" : '*.SLDDRW',
    "sldasm" : '*.SLDASM',
    "sldall" : '*.SLD*',
    "ncprog" : '*.NC',
    "caddwg" : '*.DWG',
    "anyft"  : '*.*'
}

EXECUTABLES = {
    "edrawings"   :   Path(r"C:\Program Files\SOLIDWORKS Corp\eDrawings\EModelViewer.exe"),
    "solidworks"  :   Path(r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS\SLDWORKS.exe"),
    "editnc"      :   Path(r"C:\Program Files (x86)\editNC11\editNC11.exe"),
    "cimco"       :   Path(r"C:\CIMCO\CIMCOEdit8\CIMCOEdit.exe"),
    "vim"         :   Path(r"C:\Program Files (x86)\Vim\vim82\gvim.exe")
}

DEFAULT_NC_EDITOR = EXECUTABLES['cimco']

MESSAGES = {
    "no_results"    : 'No files matching %s found in %s',
    "msg_exe"       : 'Opening file %s with %s',
    "prompt"        : '>>> ',
    "promt_file"    : 'Please choose a file:\n',
    "promt_prog"    : 'Which program would you like to use?\n',
    "itemno"        : "Enter an item number (q to quit): ",
    "where_search"  : "Where do you want to search?",
}
MSG_DELAY = 3 # seconds to show an error message

# main menu
SEARCH_OPTIONS = [
    'Everywhere',
    'Legacy CAD',
    'The Vault',
    'NC Program Library',
    'Personal Reference',
    'EdgeCAM files',
    'Quit'
]