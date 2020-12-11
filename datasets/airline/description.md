## Airline Columns
* FlightDate	Flight Date (yyyymmdd)
* Reporting_Airline	Unique Carrier Code. When the same code has been used by multiple carriers, a numeric suffix is used for earlier users, for example, PA, PA(1), PA(2). Use this field for analysis across a range of years.
* OriginAirportID	Origin Airport, Airport ID. An identification number assigned by US DOT to identify a unique airport. Use this field for airport analysis across a range of years because an airport can change its airport code and airport codes can be reused.
* DestAirportID	Destination Airport, Airport ID. An identification number assigned by US DOT to identify a unique airport. Use this field for airport analysis across a range of years because an airport can change its airport code and airport codes can be reused.
* DepDelayMinutes	Difference in minutes between scheduled and actual departure time. Early departures set to 0.
* ArrDelayMinutes	Difference in minutes between scheduled and actual arrival time. Early arrivals set to 0.
* Cancelled	Cancelled Flight Indicator (1=Yes)
* CancellationCode	Specifies The Reason For Cancellation
* Diverted	Diverted Flight Indicator (1=Yes)		
* CarrierDelay	Carrier Delay, in Minutes
* WeatherDelay	Weather Delay, in Minutes
* NASDelay	National Air System Delay, in Minutes	
* SecurityDelay	Security Delay, in Minutes
* LateAircraftDelay	Late Aircraft Delay, in Minutes