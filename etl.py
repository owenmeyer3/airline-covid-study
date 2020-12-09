import pandas as pd
from os import listdir
#--------------AIRLINE-------------------
airlineDataPath = 'datasets/airline/data/'
try:
    #get list of airline data csv files
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

    # Remove weather related cancellations
    tempAirDF = tempAirDF[(tempAirDF['CANCELLATION_CODE'] != 'B')]

    # Create TOTAL_DELAY column as a sum of all flight delays besides WEATHER_DELAY
    tempAirDF['total_delay'] = tempAirDF['CARRIER_DELAY'] + tempAirDF['NAS_DELAY'] + tempAirDF['SECURITY_DELAY'] + tempAirDF['LATE_AIRCRAFT_DELAY']

    # Remove unneeded columns
    # All columns: "FL_DATE","OP_UNIQUE_CARRIER","ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_DELAY_NEW","ARR_DELAY_NEW","CANCELLED","CANCELLATION_CODE","DIVERTED","CARRIER_DELAY","WEATHER_DELAY","NAS_DELAY","SECURITY_DELAY","LATE_AIRCRAFT_DELAY","Unnamed 14"
    tempAirDF = tempAirDF.drop(["ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_DELAY_NEW","ARR_DELAY_NEW","CANCELLATION_CODE","DIVERTED","CARRIER_DELAY","WEATHER_DELAY","NAS_DELAY","SECURITY_DELAY","LATE_AIRCRAFT_DELAY", "Unnamed: 14"], axis=1)
 
    # Replace NaN TOTAL_DELAY
    tempAirDF['total_delay'] = tempAirDF['total_delay'].fillna(0)

    # Rename date column
    tempAirDF = tempAirDF.rename(columns={"FL_DATE":"date", "OP_UNIQUE_CARRIER":"carrier", "CANCELLED":"cancelled"})
    # If this is the first dataset, create all-date dataframe
    if i == 0:
        airDF = tempAirDF
    # Else, append to all-date dataframe
    else:
        airDF.append(tempAirDF)
print(airDF.head(10))
#--------------COVID-------------------
covidDataPath =  'datasets/covid-19/covid_us_county.csv'
covid_df = pd.read_csv(covidDataPath)

# Take only date and cases columns and sum cases
covid_df = covid_df.groupby(['date'])[['cases']].sum()

#--------------Join on date------------


#--------------Plot date vs [total case, all airline delay, AA delay, DL delay, WN delay, UA delay, nk delay, f9 dealy]-------
