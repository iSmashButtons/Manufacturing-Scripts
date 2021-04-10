#!/usr/bin/python3
# The Matchstick Game
# 
# Programmed by Dennis Chaves
# dennis@dennischaves.xyz
# 
# A simulation of manufacturing flow based on "The Matchstick Game" as described in the book "The Goal" by Eliyahu Goldratt.
# 
# We have a production line with a "stockroom" on one end, the customer on the other, and 5 workstations (cells) in between.
# We simulate the stockroom "recieving an order" by rolling dice. He pulls material (matchsticks) and passes it to cell-1.
# To simulate variation in production processes from day-to-day, cell-1 rolls dice to determine how many widgets (matchsticks) he can "process" today.
# The "processed" widgets are passed to the next cell.
# Cell-2 also rolls dice to determine how many widgets he processes and moves to cell-3 and so on.
# Each cell can only process what they have and can only process up to the amount rolled.
# If a cell rolls 6 but only has 3 widgets, he only processes/moves 3 widgets.
# Conversely, if a cell rolls 3 while having 6 widgets, only 3 widgets are processed and 3 remain at the cell.

import random
import math

### FUNCTIONS ###
def rollDice(dice):
    """ Roll `dice` number of 6-sided dice and return the resulting sum. """
    result = 0
    for die in range(dice):
        result += random.randint(1,6)
    return result

### INPUT ###
# wip index 0: stockroom; index 1-5: mfg cells; index 6: customer.
wip = [0] * 7
# number of days (cycles) to simulate (run loop)
DAYS = int(input('Number of weeks to run simulation: ')) * 5
# number of dice used for each roll
DICE = int(input('Number of dice to use on each roll: '))

### MAIN PROGRAM ###
qtyOrdered = 0
for day in range(DAYS):
    # stockroom: Order in!
    wip[0] = rollDice(DICE)
    qtyOrdered += wip[0]
    #print(f'Day {day+1}!')
    #print(f'Order in for {wip[0]} widgets! {wip}')
    wip[0], wip[1] = 0, (wip[0] + wip[1]) # Move matchsticks to cell 1

    # cell-loop
    for i in range(1,6):
        #print(f'\nProduction Line Snapshot:\n{wip}\n')
        #print(f'Cell {i} inventory: {wip[i]}')
        nMove = rollDice(DICE) # Number of matchsticks to be moved
        #print(f'Cell {i} can process {nMove} widgets today.')
        if nMove >= wip[i]:
            # Move everything to next cell
            wip[i], wip[i+1] = 0, (wip[i+1] + wip[i])
            #print(f'I have just enough or not enough, so I will move what I have to cell {i+1}')
        else:
            wip[i], wip[i+1] = (wip[i] - nMove), (wip[i+1] + nMove)
            #print(f'I moved {nMove} to cell {i+1} and I have {wip[i]} remaining.')
    #print(f'\nShift over! end of day {day+1}. We shipped {wip[6]} finished products to date.\n')

# print results
totalWIP = 0
for work in wip[1:6]:
    totalWIP += work

print('\n' + ' SUMMARY RESULTS '.center(60,'#'))

print(
    'days'.center(12),
    'Ordered'.center(12),
    'Shipped'.center(12),'% shipped'.center(12),
    'WIP'.center(12)
)
print(
    f'{DAYS}'.center(12),
    f'{qtyOrdered}'.center(12),
    f'{wip[6]}'.center(12),
    f'{math.floor(((wip[6] / qtyOrdered) * 100))}%'.center(12),
    f'{totalWIP}'.center(12)
)
