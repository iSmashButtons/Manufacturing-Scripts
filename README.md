# Manufacturing Scripts
A collection of programs/scripts I've used on the job.

## ncArchiver

A simple script to archive the shop's NC code library into a zip file. Windows Task Scheduler runs this script automatically every other week. It has saved us from many accidental file-overwrite scares.

## Spring Length Data (sld.py)

Is a data entry & recall program. Part of the process of creating spring-energized seals is determining how long to cut the spring, so that it can be welded end-to-end to create a circle and then inserted into the seal jacket. I was being approached every day by assemblers asking me to calculate this length for them. I created this program so that I would not have to calculate the length more than once.

The user inputs an item number. If this is the first time the item number has been entered, the user is asked to supply more information about spring type, and diameter of installation. This information is then saved to a CSV so it can be recalled later or viewed by my other coworkers. If the item number is already in the CSV file, the program returns this information in a table.
