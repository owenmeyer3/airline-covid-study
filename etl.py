import pandas as pd
from os import listdir
import matplotlib.pyplot as plt
from datetime import datetime
#--------------AIRLINE-------------------
airlineDataPath = 'datasets/airline/data/'
#Select-airlines = American:AA Delta:DL Southwest:WN United:UA Spirit:NK Frontier: F9
carrierList = ['AA','DL','WN','UA','NK','F9']
try:
    # Get list of airline data csv files
    airDataFileNames = listdir(airlineDataPath)
except:
    print('files names in ' + airlineDataPath + ' not found')

### Import monthly dataframe, clean monthly dataframe and combine into all-date dateframe from 2018-01 to 2020-09
carrierDFs = {}
isFirstMonth = True
for name in airDataFileNames:
    ## Get monthly dataframe
    try:
        monthAirDF = pd.read_csv(airlineDataPath + name, dtype={'FL_DATE':"string"})
        #monthAirDF['FL_DATE'] = monthAirDF['FL_DATE'].astype(str)
    except:
        print('file in ' + airlineDataPath + ' not found')

    ## Clean monthly dataframe
    # Remove non-select airlines
    monthAirDF = monthAirDF[monthAirDF['OP_UNIQUE_CARRIER'].isin(carrierList)]
    # Remove weather related cancellations
    monthAirDF = monthAirDF[(monthAirDF['CANCELLATION_CODE'] != 'B')]

    # Create TOTAL_DELAY column as a sum of all flight delays besides WEATHER_DELAY
    monthAirDF['total_delay'] = monthAirDF['CARRIER_DELAY'] + monthAirDF['NAS_DELAY'] + monthAirDF['SECURITY_DELAY'] + monthAirDF['LATE_AIRCRAFT_DELAY']

    # Remove unneeded columns
    # Desired Columns: "FL_DATE", "OP_UNIQUE_CARRIER", "CANCELLED", "total_delay"
    # All columns: "FL_DATE","OP_UNIQUE_CARRIER","ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_DELAY_NEW","ARR_DELAY_NEW","CANCELLED","CANCELLATION_CODE","DIVERTED","CARRIER_DELAY","WEATHER_DELAY","NAS_DELAY","SECURITY_DELAY","LATE_AIRCRAFT_DELAY","Unnamed 14", "total_delay"
    monthAirDF = monthAirDF.drop(["ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_DELAY_NEW","ARR_DELAY_NEW","CANCELLATION_CODE","DIVERTED","CARRIER_DELAY","WEATHER_DELAY","NAS_DELAY","SECURITY_DELAY","LATE_AIRCRAFT_DELAY", "Unnamed: 14"], axis=1)
    
    # Replace NaN TOTAL_DELAY
    monthAirDF['total_delay'] = monthAirDF['total_delay'].fillna(0)
    
    # average the cancelled flights and delay times per day per airline(this makes date an object)
    monthAirDF["FL_DATE"] = monthAirDF["FL_DATE"].astype("string")
    monthAirDF = monthAirDF.groupby(["FL_DATE", "OP_UNIQUE_CARRIER"]).agg({"CANCELLED":["mean"],"total_delay":["mean"]}).reset_index()


    # Remove outer column index (this makes date an object)
    monthAirDF.columns = monthAirDF.columns.droplevel(0)

    # Rename columns and covert datatypes
    monthAirDF.columns = ["date", "carrier", "cancelled_rate", "total_delay"]
    monthAirDF = monthAirDF.astype({'date':'string', 'carrier':'string'})
    
    print(name + ' - monthAirDF added')

    # Break allAirDF into carrierDF
    for carrier in carrierList:
        monthCarrierDF = monthAirDF[monthAirDF['carrier'] == carrier]
        monthCarrierDF = monthCarrierDF.drop(columns=['carrier'])

        #Join monthCarrierDFs together into modMonthAirDF
        monthCarrierDF = monthCarrierDF.rename(columns={"cancelled_rate": "cancelled_rate_" + carrier, "total_delay": "total_delay_" + carrier})
        
        if carrier == carrierList[0]:
            modMonthAirDF = monthCarrierDF
        else:
            modMonthAirDF = modMonthAirDF.merge(monthCarrierDF, on='date', how='left', sort=False)

    # Add monthly carrier DFs to carrierDFs
    if isFirstMonth:
        modAirDF = modMonthAirDF
    # Else, monthly carrier DFs to carrierDFs
    else:
        modAirDF = modAirDF.append(modMonthAirDF, ignore_index = True)
    
    isFirstMonth = False

#--------------COVID-------------------
covidDataPath =  'datasets/covid-19/covid_us_county.csv'
covid_df = pd.read_csv(covidDataPath)

# Take only date and cases columns and sum cases(this makes date an object)
covid_df = covid_df.groupby(['date'])[['cases']].sum().reset_index()
covid_df = covid_df.astype({'date':'string'})


#--------------Join on date------------
# Combine the data into a single dataset
study_data_complete = modAirDF.merge(covid_df, how="left", on=["date", "date"])

# Fill NaN cases with 0
study_data_complete['cases'] = study_data_complete['cases'].fillna(0)

print(study_data_complete)
#--------------Plot date vs [total case, all airline delay, AA delay, DL delay, WN delay, UA delay, nk delay, f9 dealy]-------
x = study_data_complete['date']
y1 = study_data_complete['cancelled_rate_AA']
y2 = study_data_complete['cases']

study_data_complete.plot(x='date',y='cancelled_rate_AA')
study_data_complete.plot(x='date',y='cases', secondary_y=True)

plt.show()

