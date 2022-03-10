from functions import *
from config import *

# TODO: PEP8 main, functions, config
# TODO: Implement logging

while True:
    clear_screen()
    item = get_item_number()
    item = item.upper()

    clear_screen()
    search_location = get_search_location()

    clear_screen()
    if search_location == SEARCH_OPTIONS[0]: # everything
        cad_results = get_cad_results(item)
        vault_results = search(item, SEARCH_LOCATIONS['awc_vault'], FILETYPES['sldall'])
        ncprog_results = search(item, SEARCH_LOCATIONS['nc_lib'], FILETYPES['ncprog'])
        pref_results = search(item, SEARCH_LOCATIONS['sld_ref'], FILETYPES['sldall'])
        ecam_results = get_ecam_results(item)

        results_selection = results_by_location_menu(item, cad_results, vault_results, pref_results, ncprog_results, ecam_results)
        results_selection = results_selection.lower()

        # select file and launch based on results selection
        if 'cad' in results_selection:
            select_file_launch_exe(cad_results)
        elif 'vault' in results_selection:
            select_file_launch_exe(vault_results)
        elif 'ref' in results_selection:
            select_file_launch_exe(pref_results)
        elif 'progs' in results_selection:
            select_file_launch_exe(ncprog_results)
        elif 'cam' in results_selection:
            select_file_launch_exe(ecam_results)
        elif 'quit' in results_selection:
            continue

    # Parse other possible choices
    elif search_location == SEARCH_OPTIONS[1]: # Legacy CAD
        cad_files = get_cad_results(item)
        select_file_launch_exe(cad_results)
    elif search_location == SEARCH_OPTIONS[2]: # The Vault
        vault_files = search(item, SEARCH_LOCATIONS['awc_vault'], FILETYPES['sldall'])
        select_file_launch_exe(vault_files)
    elif search_location == SEARCH_OPTIONS[3]: # nc programs
        nc_programs = search(item, SEARCH_LOCATIONS['nc_lib'], FILETYPES['ncprog'])
        if len(nc_programs) == 0:
            print('No programs found')
            continue
        select_file_launch_exe(nc_programs)
    elif search_location == SEARCH_OPTIONS[4]: # personal reference
        reference_files = search(item, SEARCH_LOCATIONS['sld_ref'], FILETYPES['sldall'])
        select_file_launch_exe(reference_files)
    elif search_location == SEARCH_OPTIONS[4]: # EdgeCAM files
        ecam_files = search(item, SEARCH_LOCATIONS['edgecam'], FILETYPES['sldall'])
        select_file_launch_exe(ecam_files)
    else:
        continue