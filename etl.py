import pandas as pd
from os import listdir
#--------------AIRLINE-------------------
###get list of airline data csv files
airlineDataPath = 'datasets/airline/data/'
try:
    airDataFileNames = listdir(airlineDataPath)
except:
    print('files names in ' + airlineDataPath + ' not found')

### Import monthly dataframe, clean monthly dataframe and combine into all-date dateframe from 2018-01 to 2020-09
for i, name in enumerate(airDataFileNames):
    ## Get monthly dataframe
    try:
        tempAirDF = pd.read_csv(airlineDataPath + name)
    except:
        print('file in ' + airlineDataPath + ' not found')
    ## Clean monthly dataframe
    # Remove non-select airlines -- Select-airlines = American:AA Delta:DL Southwest:WN United:UA Spirit:NK Frontier: F9
    tempAirDF = tempAirDF[(tempAirDF['OP_UNIQUE_CARRIER'] == 'AA') | (tempAirDF['OP_UNIQUE_CARRIER'] == 'DL') | (tempAirDF['OP_UNIQUE_CARRIER'] == 'WN') | (tempAirDF['OP_UNIQUE_CARRIER'] == 'UA') | (tempAirDF['OP_UNIQUE_CARRIER'] == 'NK') | (tempAirDF['OP_UNIQUE_CARRIER'] == 'F9')]

    # If this is the first dataset, create all-date dataframe
    if i == 0:
        airDF = tempAirDF
    # Else, append to all-date dataframe
    else:
        airDF.append(tempAirDF)


#--------------COVID-------------------


#--------------Join on date------------


#--------------Plot date vs [total case, all airline delay, AA delay, DL delay, WN delay, UA delay, nk delay, f9 dealy]-------
