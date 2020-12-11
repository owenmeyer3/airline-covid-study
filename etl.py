import pandas as pd
from os import listdir
import matplotlib.pyplot as plt
from datetime import datetime
from sqlalchemy import create_engine
import psycopg2
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
    try:
        # get airline data for each month
        monthAirDF = pd.read_csv(airlineDataPath + name, dtype={'FL_DATE':"string"})
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
    monthAirDF = monthAirDF.drop(["ORIGIN_AIRPORT_ID","DEST_AIRPORT_ID","DEP_DELAY_NEW","ARR_DELAY_NEW","CANCELLATION_CODE","DIVERTED","CARRIER_DELAY","WEATHER_DELAY","NAS_DELAY","SECURITY_DELAY","LATE_AIRCRAFT_DELAY", "Unnamed: 14"], axis=1)
    
    # Replace NaN with 0 for TOTAL_DELAY (this makes date an object)
    monthAirDF['total_delay'] = monthAirDF['total_delay'].fillna(0)
    monthAirDF["FL_DATE"] = monthAirDF["FL_DATE"].astype("string")

    # Average the cancelled flights and delay times per day per airline
    monthAirDF = monthAirDF.groupby(["FL_DATE", "OP_UNIQUE_CARRIER"]).agg({"CANCELLED":["mean"],"total_delay":["mean"]}).reset_index()

    # Remove outer column index (this makes date an object)
    monthAirDF.columns = monthAirDF.columns.droplevel(0)

    # Rename columns and covert datatypes
    monthAirDF.columns = ["date", "carrier", "cancelled_rate", "total_delay"]
    monthAirDF = monthAirDF.astype({'date':'string', 'carrier':'string'})

    # Break allAirDF into carrierDF
    for carrier in carrierList:
        monthCarrierDF = monthAirDF[monthAirDF['carrier'] == carrier]
        monthCarrierDF = monthCarrierDF.drop(columns=['carrier'])

        # Rename columns for specific airline
        monthCarrierDF = monthCarrierDF.rename(columns={"cancelled_rate": "cancelled_rate_" + carrier, "total_delay": "total_delay_" + carrier})

        # Join monthCarrierDFs together into modMonthAirDF
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

    # Set not first month for second iteration of months
    isFirstMonth = False

#--------------COVID-------------------
# Get covid date
covidDataPath =  'datasets/covid-19/covid_us_county.csv'
covid_df = pd.read_csv(covidDataPath)

# Take only date and cases columns and sum cases(this makes date an object, convert date back to string)
covid_df = covid_df.groupby(['date'])[['cases']].sum().reset_index()
covid_df = covid_df.astype({'date':'string'})


#--------------Join on date------------
# Combine the data into a single dataset
study_data_complete = modAirDF.merge(covid_df, how="left", on=["date", "date"])

# Fill NaN cases with 0
study_data_complete['cases'] = study_data_complete['cases'].fillna(0)

print(study_data_complete)

#--------------Plot date vs [total cases, flight cancellations per airline], [total cases, flight delays per airline]-------
#define dates series as datetime objects
dates = pd.to_datetime(study_data_complete['date'], format='%Y-%m-%d')

# create figure and Flight Cancellation axis object with subplots()
fig,ax1 = plt.subplots()

ax1.plot(dates, study_data_complete['cancelled_rate_AA'], label='American')
ax1.plot(dates, study_data_complete['cancelled_rate_DL'], label='Delta')
ax1.plot(dates, study_data_complete['cancelled_rate_WN'], label='Southwest')
ax1.plot(dates, study_data_complete['cancelled_rate_UA'], label='United')
ax1.plot(dates, study_data_complete['cancelled_rate_NK'], label='Spirit')
ax1.plot(dates, study_data_complete['cancelled_rate_F9'], label='Frontier')

# Create Covid Cases axis object
ax2 = ax1.twinx()
ax2.plot(dates, study_data_complete['cases'], label='Covid Cases')

# Format Text on Plot
plt.title("Flight Cancellations vs. US Covid Cases per Day")
ax1.set_xlabel("date")
ax1.set_ylabel("Cancelled Flight Rate")
ax2.set_ylabel("Covid Cases")
ax1.legend(loc='upper left')
ax2.legend(loc='upper center')
plt.show()

# create figure and Flight Delay axis object with subplots()
fig,ax3 = plt.subplots()

ax3.plot(dates, study_data_complete['total_delay_AA'], label='American')
ax3.plot(dates, study_data_complete['total_delay_DL'], label='Delta')
ax3.plot(dates, study_data_complete['total_delay_WN'], label='Southwest')
ax3.plot(dates, study_data_complete['total_delay_UA'], label='United')
ax3.plot(dates, study_data_complete['total_delay_NK'], label='Spirit')
ax3.plot(dates, study_data_complete['total_delay_F9'], label='Frontier')

# Create Covid Cases axis object
ax4 = ax3.twinx()
ax4.plot(dates, study_data_complete['cases'], label='Covid Cases')

# Format Text on Plot
plt.title("Flight Delays vs. US Covid Cases per Day")
ax3.set_xlabel("date")
ax3.set_ylabel("Average Delay Time (min)")
ax4.set_ylabel("Covid Cases")
ax3.legend(loc='upper left')
ax4.legend(loc='upper center')
plt.show()

#create engine
engine = create_engine('postgres://postgres:Flyingtwig5412@localhost:5432/Airline_Covid_Study')
conn = engine.connect()

#rename df
test = engine.table_names() 
Airline_Covid_Study = study_data_complete

#create string for SQL table
createString = '''
	CREATE TABLE airlines_covid (
	date VARCHAR(20),
	cancelled_rate_AA FLOAT(23),
	total_delay_AA FLOAT(23),
	cancelled_rate_DL FLOAT(23),
	total_delay_DL FLOAT(23),
	cancelled_rate_WN FLOAT(23),
	total_delay_WN FLOAT(23),
	cancelled_rate_UA FLOAT(23),
	total_delay_UA FLOAT(23),
	cancelled_rate_NK FLOAT(23),
	total_delay_NK FLOAT(23),
	cancelled_rate_F9 FLOAT(23),
	total_delay_F9 FLOAT(23),
	cases int)
'''


#conn.execute(createString)

#table_name = 'airlines_covid'
#study_data_complete.to_sql(
  #  table_name,
   # engine,
   # if_exists='replace',
   # index=False,
   # chunksize=500, 
#)
 

