#!/usr/bin/python3
"""Spring Length Database (SLD)
Enter a drawing number and SLD will display assembly information available.
If no information is available, it can be collected from the user.

For seals with two face springs, append `-i` or `-o` (inner/outer) to the drawing name to differntiate between the inner and outer spring diameters
"""

import math
import sys
import re
import time

# ===== CONFIG ===== #
NAME='SES spring length database'
VERSION='0.2'
CSV_PATH=r'C:\Users\chavesd\springLengthData\springData.csv'
CSVHEADER=''
cantileverV={ '000':0.020, '100':0.030, '200':0.040, '300':0.055, '400':0.075, '500':0.150 }
cantileverU={ 'B':0.020, 'C':0.028, 'D':0.045, 'E':0.050, 'F':0.102, 'G':0.182 }
BOMregex=r'\d{3}MS|\d{3}[B-G]|\d{3}X\d{3}X\d{3}' # cant-V | cant-U | helical

# ===== FUNCTIONS ===== #
def welcomeSign():
    """Displays a welcome message"""
    for i in range(len(NAME)):
        print('#',end='')
    print('\n'+NAME)
    print('Version:',VERSION.rjust(len(NAME) - len('Version: ')))
    for i in range(len(NAME)):
        print('#',end='')
    print('')
    print('USAGE NOTES:')
    print('For seals with two face springs, append `-i` or `-o` (inner/outer) to the drawing name to differntiate between the inner and outer spring diameters')

def csv2dict(CSVfile):
    """converts the springData CSV into a dictionary
    The dictionary looks like this:
    {
        drawingNumber:{springBomb:'500MS', springDia:1.234, cutLen:5.678}
    }
    """
    global CSVHEADER
    csvArray=open(CSVfile,'r').read()
    csvArray = csvArray.split('\n')
    CSVHEADER = csvArray[0]
    # first line is CSV table header, remove it.
    del csvArray[0]

    # create 2d array
    for i in range(len(csvArray)):
        csvArray[i] = csvArray[i].split(',')

    # create dictionary
    csvDict={}
    for i in range(len(csvArray)):
        csvDict[csvArray[i][0]]={
                'springBOM':csvArray[i][1],
                'springDia':csvArray[i][2],
                'cutLen':csvArray[i][3]
                }
    return csvDict

def printExistingData(drawingNumber):
    """prints available data for `drawingNumber`"""
    # TODO: prettify text output with r/ljust functions
    global springDB
    print('\n' + ' %s '.center(30,'=') %drawingNumber)
    print('Spring: '.ljust(20,'.') + ' ' + springDB[drawingNumber]['springBOM'])
    print('Spring Diameter: '.ljust(20,'.') + ' ' + str(springDB[drawingNumber]['springDia']))
    print('Cut Length: '.ljust(20,'.') + ' '  + str(springDB[drawingNumber]['cutLen']), end='\n\n')
    #for k,v in springDB[drawingNumber].items():
        #print(k +':\t'+str(v))
    return None

def newDBentry(drawingNumber):
    """add new spring data to springDB dictionary.
    Returns a dictionary with keys: `springBOM`, `springDia`, and `cutLen`."""
    global springDB
    newEntry = {drawingNumber:{}}
    # TODO: check validity of input
    newEntry[drawingNumber]['springBOM'] = input('Enter spring ID from BOM (eg. 500MS, 316D, 003x040x100): ').upper()
    newEntry[drawingNumber]['springDia'] = float(input('Enter spring diameter: '))

    # cantilever-V springs
    if re.match(r'\d{3}MS',newEntry[drawingNumber]['springBOM']) != None:
        series = (newEntry[drawingNumber]['springBOM'])[:3]
        diameter = newEntry[drawingNumber]['springDia']
        C = cantileverV[series]
        if series == '500':
            newEntry[drawingNumber]['cutLen'] = round( float(diameter * math.pi),ndigits=3)
            print('\nNew Database Entry:')
            print(newEntry[drawingNumber])
            return newEntry[drawingNumber]
        else:
            newEntry[drawingNumber]['cutLen'] = round( float( (diameter * math.pi) + C),  ndigits=3)
            print('\nNew Database Entry:')
            print(newEntry[drawingNumber])
            return newEntry[drawingNumber]
    # cantilever-U springs
    elif re.match(r'\d{3}[B-G]',newEntry[drawingNumber]['springBOM']) != None:
        series = (newEntry[drawingNumber]['springBOM'])[3:4]
        diameter = newEntry[drawingNumber]['springDia']
        C = cantileverU[series]
        if series == 'F' or series == 'G':
            newEntry[drawingNumber]['cutLen'] = round( float(diameter * math.pi),ndigits=3)
            return newEntry[drawingNumber]
        else:
            newEntry[drawingNumber]['cutLen'] = round( float( (diameter * math.pi) + C),  ndigits=3)
            print('\nNew Database Entry:')
            print(newEntry[drawingNumber])
            return newEntry[drawingNumber]
    # helical springs 003x040x100
    elif re.match(r'\d{3}X\d{3}X\d{3}',newEntry[drawingNumber]['springBOM']) != None:
        diameter = newEntry[drawingNumber]['springDia']
        C = int((newEntry[drawingNumber]['springBOM'])[4:7]) * (10 ** -3)
        newEntry[drawingNumber]['cutLen'] = round( float( (diameter * math.pi) + C),  ndigits=3)
        return newEntry[drawingNumber]
    # TODO: add J-springs elif
    # TODO: add rayco spring elif
    else:
        return -1
    
def appendToCSV(x):
    """
    Convert new entry from dictionary to a CSV string and append to CSV file.
    new entry looks like:
    {'FC01N1234': {'springBOM': '300MS', 'springDia': 1.234, 'cutLen': 3.932}}
    """
    global dwgN
    output = [''] * 4
    #output[0],output[1],output[2],output[3] = dwgN, x[dwgN]['springBOM'], str(x[dwgN]['springDia']), str(x[dwgN]['cutLen'])
    output[0],output[1],output[2],output[3] = dwgN, x['springBOM'], str(x['springDia']), str(x['cutLen'])
    # output looks like:
    # ['FC01N1234', '300MS', '1.234', '3.932']

    # append to file:
    csvFile = open(CSV_PATH,'a')
    print('\n CSV output:')
    print(output, end='\n')
    csvFile.write('\n' + ','.join(output))

# ===== MAIN PROGRAM ===== #
welcomeSign()

# create a dictionary from the csv file on disk.
springDB=csv2dict(CSV_PATH)

while True:
    # Get drawing number from user
    dwgN = input('Enter drawing number (q to quit): ').upper()
    if dwgN in springDB:
        printExistingData(dwgN)
    elif dwgN == 'Q':
        quit()
    else:
        reply=input('\nNo data for %s\nAdd to the database (y/n)? ' %dwgN).lower()
        if re.match('y|1',reply) != None:
            # appends a new key on the springDB dictionary
            #newEntry = {dwgN:newDBentry(dwgN)}
            #appendToCSV(newEntry)
            springDB[dwgN] = newDBentry(dwgN)
            appendToCSV(springDB[dwgN])
            printExistingData(dwgN)
        else:
            print('No new entry created')
            time.sleep(2.5)
