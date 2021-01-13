# manufacturing
A collection of programs/scripts I've used on the job to solve manufacturing problems.

## What's in here?

### ncArchiver

A simple script to archive the shop's NC code library into a zip file. Windows Task Scheduler runs this script automatically every other week. It has saved us from many accidental file-overwrite scares.

### Spring Length Data

Is a simple data entry & recall program. Part of the process of created spring-energized seals is determining how long to cut the spring, so that it can be welded and inserted into the seal jacket. I was being approached every day by assemblers asking me to calculate this length for them. I created this program so that I would not have to calculate the length more than once. 

The user inputs an item number. If this spring length was calculated before, the program returns this information in a table. If this is the first time the program has seen the part, the user is asked for supply more information about spring type, and diameter where spring is to be installed. This information is then saved to a CSV so it can be recalled later or viewed by my other coworkers.

**Room for improvement:** as it is now, the program loads the entire CSV into memory. This could be a problem once the file becomes very large. In the future I plan to change this so that the CSV is searched through line-by-line when needed, instead of loading the whole file into memory.
