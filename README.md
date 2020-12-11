# Airline-Study

#ETL

In our project we wanted to study the effect that the COVID-19 pandemic had on flight cancellations and flight delays among the
4 largest Airlines in the United States; we also included Spirit & Frontier. 

#Extract

We found our airline data on the Bureau of Transportation and our COVID data on Kaggle. 
Both datasets were downloaded as CSVs. All of the Airline data was downloaded month-by-month. 
We later transformed the data by merging all of the airline data into a single pandas table, the process will be found below in our "transform" section.

#Transform

The top 4 largest airlines in the US are American, Delta, Southwest & United. We decided to include Spirit & Frontier out of curosity.
So, we created our monthly airline data using only flights/scheduled flights from these airlines.

In our next step, we cleaned our dataframe by limiting the data to the timeframe 2018-01 to 2020-09
In summary, we looped through all of the monthly CSVs dropping all of the carriers that were not in our list and dropping all other besides the columns that we were required for our study.

Within each month CSV, after it dropped all unnesscary columns and carriers. it was appended into a "master" dataframe.


#Observations

We used Kaggle to pull both our COVID and Airline Data – there were quite a few columns of airline data that we didn’t find relevant (Weather Delays/Cancellations, departure/arrival airports)

Would be interesting to make note of destination and departure airports to see if some states are affected more than others. The view of COVID has become heavily politicized, and we thought it would be interesting, for future, to see if there’s any major difference in delay data by red or blue state. 

We saw that there were a lot more cancellations than there were delays. This is kind of an interesting observation as it seems to suggest that these airlines all have a process in place for loading their planes in a timely manner, even while COVID is surging.
