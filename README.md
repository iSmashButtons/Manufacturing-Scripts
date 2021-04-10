# Manufacturing Scripts
A collection of programs/scripts I've created and used on the job.

## ncArchiver.py

A simple script to archive the shop's NC code library into a zip file. Windows Task Scheduler runs this script automatically every other week. It has saved us from many accidental file-overwrite scares.

## Spring Length Data (sld.py)

Is a data entry & recall program. Part of the process of creating spring-energized seals is determining how long to cut the spring, so that it can be welded end-to-end to create a circle and then inserted into the seal jacket. I was being approached every day by assemblers asking me to calculate this length for them. I created this program so that I would not have to calculate the length more than once.

The user inputs an item number. If this is the first time the item number has been entered, the user is asked to supply more information about spring type, and diameter of installation. This information is then saved to a CSV so it can be recalled later or viewed by my other coworkers. If the item number is already in the CSV file, the program returns this information in a table.

## SES-Finder (sesf.py)

A script to help me quickly find files in several locations based on a single item number. I use this on the job several times a day. What inspired the creation of this script was the tedium of searching for the files I needed to work with on a daily basis. Windows File Explorer is one of the worst file managers around, and SolidWork's PDM system is very slow. It can take several minutes to load and navigate to one of the several locations where the files I need might be. And once I get there, the part number I"m looking for might now be there. My job revolves around getting product out on time, so every minute counts. I needed a quicker way to find all the files I could possibly want related to a certain part number.

The way `sesf` works is you execute the program and pass in an item number. It will then go and search for this item number in four locations: the AutoCAD drawing directory, the SolidWorks PDM Vault, the NC Program Library, and my personal reference models. `sesf` returns a list of these locations and how many matching files it found in each place. From there the user can select which file to open. Optionally, several flags can also be passed in to limit the search to a specific location.

I am a neophyte programmer. If you are a seasoned coder familiar with Python I would love to get your feedback on my script. Thanks for checking it out!

## NC-linter

*nc-linter* is a BASH script with a big chunk of AWK script inside doing most of the work. In the configuration section, you point it to a directory that contains the NC programs you want to lint. The AWK script then reads through each file and checks for common mistakes. If any are found, the script also fixes the error and logs the changes made. The fixed programs are written to a separate directory, where they can be double-checked by a human before replacing the originals. I got a lot of help on this one from my friend Paul in England who is a retired sysadmin and AWK expert. I'm not sure if BASH/AWK were the best tools for this job, but I was learning to use them at the time. *nc-linter* checks for these errors: 

- missing Transmission Start marker (%)
- program address is ":" instead of "O"
- extraneous transmission markers (%)
- leading/trailing whitespace on lines
- open comments
- double-decimals (`X10.0.0`)
- missing address (number without a corresponding address, eg: `0.1234`)
- decimal values exceeding 4 digits.

A log is output for each file. The report lists a terse error description along with the line numbers where the error appears. Some "errors", like leading/trailing spaces, don't cause any trouble at the machine but they are ugly. For these errors the total number of lines is output instead of unique line numbers.

## cabinet-project

At the start of SES in Groveland, we inherited a cabinet full of bins with tools. Most of the tools were custom grinds. There were several tools to a bin and the bins were labeled A1-60, B1-60, etc. The problem was that no one knew which tools we for what job, and the bins were shaken around turn transport. So even on the rare occasion when we came accross a program that referenced a tool in a bin here, more often than not the tool located in that bin had nothing to do with the job at hand. This script is an attempt to sort out this cabinet. I grep'd through every program looking for a pattern matching the bin labels: A24, B16, C32, et cetera. This produced a list of programs where a tool was referenced. There were many duplicate matches so I filtered these out with the `uniq` program. The end result was four files with comma-delimited lists.

- `bins_A.uniq.r1`
- `bins_B.uniq.r1`
- `bins_C.uniq.r1`
- `bins_D.uniq.r1`

Each list item displays the filename, the line number on which a bin was mentioned, the comment containing a bin number. In that order. The file names from this list are cross-referenced with a CSV to find the appropriate part number for that program file. All this information is then output to another list which will be used to sort out the cabinet. This last list I can use to look up a part drawing. I can then pull the tool and compare it to the drawing, if it looks like a useful tool for that job, I kept it. Otherwise I threw it out.

`bin-reporter.sh` takes one of the above mentioned lists in argument and process it, producing a new list use to sort out the tools in the cabinet.

## GMACRO

This is a collection of "G-Macro" programs I've written to create fixtures and gauges in the shop. They are very similar to Macro NC programs used on many CNC controls, however instead of being run on a CNC machine these G-Macro programs are interpreted by the EditNC NC-code editor. The editor interprets the macro and produces the NC code. These programs produce a nicer end product than cutting one by hand, while also requireing far less time than writing out a program manually every time you needed to make something. 
