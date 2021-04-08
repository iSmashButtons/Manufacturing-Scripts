#ID GAGE-O-MATIC 2000
#This is a python G-Code generator script
#import math
import time
import sys

print('''
======================================
//  Welcome to Gauge-O-Matic 2000!  //
//  ID-Gauge G-Code Generator       //
//  Version 2.5                     //
//  Dennis Chaves 1/4/18            //
======================================
''')

print('To start I\'ll need to know the dimensions of the tube stock you are using for this gauge.')
#time.sleep(2.5)

#Get Tube OD =========================================
while True:
    try:
        tubeOD = float(input('Enter the tube OD: '))
        break
    except ValueError:
        print('Error: you must enter a number!')
#=====================================================
#get tube ID==========================================
while True:
    try:
        tubeID = float(input('Enter the tube ID: '))
        break
    except ValueError:
        print('Error: you must enter a number!')
#=====================================================
print('<<<---------->>>')
print('Tube dimensions: ' + str(tubeOD) + ' X ' + str(tubeID))
print('<<<---------->>>')

if tubeOD < tubeID:
    print('ID cannot be larger than OD.')
    time.sleep(5)
    sys.exit()

print('Now I need the dimensions of the gauge you want to create.')

isPositive = False
while isPositive == False:
    while True:
        try:
            nomDia = float(input('Enter the nominal diameter:'))
            break
        except ValueError:
            print('Please enter a number.')
    if nomDia > 0:
        isPositive = True
    elif nomDia <= 0:
        print('you must enter a positive value!')
    else:
        print('Oh... Shit.')
        time.sleep(5)
        sys.exit()

isPositive = False #reset boolean
while isPositive == False:
    while True:
        try:
            posTol = float(input('Enter a positive Tolerance: '))
            break
        except ValueError:
            print('Please enter a number.')
    if posTol >= 0:
        isPositive = True
    elif posTol <= 0:
        print('You must enter a positive value!')
    else:
        print('Oh... Shit.')
        time.sleep(5)
        sys.exit()

isPositive = False #reset boolean
isNegative = False
while isNegative == False:
    while True:
        try:
            negTol = float(input('Enter a negative tolerance: '))
            break
        except ValueError:
            print('Please enter a number.')
    if negTol <= 0:
        isNegative = True
    elif negTol >= 0:
        print('You must enter a negative value!')
    else:
        print('Oh... Shit.')
        time.sleep(5)
        sys.exit()
    
while isPositive == False:
    while True:
        try:
            step = float(input('Enter a step height: '))
            break
        except ValueError:
            print('Please enter a number.')
    if step > 0:
        isPositive = True
    elif step <= 0:
        print('You must enter a positive value!')
    else:
        print('Oh... Shit.')
        time.sleep(5)
        sys.exit()
        
#do the math!
minDia = nomDia + negTol
maxDia = nomDia + posTol

print('''
--<<O>>--<<O>>--<<O>>--<<O>>--<<O>>--<<O>>--<<O>>--<<O>>--
OK! Let\'s review!
''')

print('>>> Tube OD = ' + str(tubeOD))
print('>>> Tube ID = ' + str(tubeID))
print('>>> Nominal Diameter = ' + str(nomDia))
print('>>> Minimum Diameter = ' + str(minDia))
print('>>> Maximum Diameter = ' + str(maxDia))
print('>>> Step height = ' + str(step))
print('^^^ Is this correct? (y/n) ^^^')
answer = input()

while True:
	if answer == 'y' or answer == 'Y':
		print('Thank you, one ID gauge coming right up!')
		break
	elif answer == 'n':
		print('Start this script over and try again.')
		print('This program will self destruct in 5 seconds.')
		time.sleep(5)
		sys.exit()
	else:
		print('type y or n')
		

#convert all variables to floaters
tubeOD = float(tubeOD)
tubeID = float(tubeID)
minDia = float(minDia)
nomDia = float(nomDia)
maxDia = float(maxDia)
step = float(step)

gCode = '''%
o00003 (ID GAUGE)
(GAUGE-O-MATIC 2000)
(DC 1/4/18)

(***DIRECTIONS***)
(SET G54 X/Z TO 0.0)
(SET NEW G50)
(CYCLE START)
(**********)

/G00 T202
/G50 Z.005
/G00 Z1.0
/M30

G54 
G00 T202 
G97 S700 M03 
X''' + str(tubeOD + 0.1) + ''' Z0.1 
G01 Z0 F0.02 
X''' + str(tubeID - 0.1) + ''' F0.005
G00 w0.01
X''' + str(tubeOD + 0.1) + ''' Z0.03 
G71 P100 Q200 U0.05 W0 D0.1 F0.006
N100 G00 X''' + str(minDia - 0.05) + ''' 
G01 Z0 
X''' + str(minDia) + ''' K-0.015
W-''' + str(step) + ''' 
X''' + str(nomDia) + ''' 
W-''' + str(step) + '''
X''' + str(maxDia) + ''' 
W-''' + str(step) + '''
X''' + str(tubeOD) + ''' F.01
N200 G00 X''' + str(tubeOD + 0.1) + '''
G00 Z1. 
G28 U0 W0 
M00 


G54 
G00 T202 
G97 S700 M03 
X''' + str(tubeOD + 0.1) + ''' Z0.1
G70 P100 Q200 F0.002 
G00 Z1. 
G28 U0 W0 
M30 
%'''

nc = open('ID-GAUGE2.NC', 'w')
nc.write(gCode)
nc.close()

print(gCode)
print('''
--<<O>>--<<O>>--<<O>>--<<O>>--<<O>>--<<O>>--<<O>>--<<O>>--
''')
print('''Thank you for using Gauge-O-Matic 2000!
This program will self destruct in 5 seconds.''')
time.sleep(5)
