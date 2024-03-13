import pandas as pd
import datetime
import glob
import sys


#df = pd.read_parquet("/data/nyctaxi/yellow_tripdata_2023-11.parquet")
df = None
for file in sorted(glob.glob("/data/nyctaxi/yellow_tripdata_2023*.parquet")):
	print("Reading", file)
	if df is None:
		df = pd.read_parquet(file)
	else:
		df = pd.concat([df, pd.read_parquet(file)])


print(df)
#print(df['tpep_pickup_datetime'])
df['date'] = df['tpep_pickup_datetime'].dt.date
#df = df[(df['date'] > datetime.date(2023,10,31)) & (df['date'] < datetime.date(2023,12,1))]
print(df.columns)
df['hour_of_day'] = df['tpep_pickup_datetime'].dt.hour
df['day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek



"""
TASK:

-find average trip distance
-find min and max fare amount

-find average fare amount per # of passengers
-find average fare amount for trips from airport
-find average congestion surcharge for each hour of the day; and for each day pf the week

-find most frequent pick up and drop off locations
-find most frequent pick up/drop off pair
-find most frequent pick up locations for night hours on weekend

- It's 3:35pm on a Saturdaty. Im at the met. How much will it cost me ant my two friends to get to the world trade
  center memorial

"""

"""
#correct awnsers
print("Avg trip distance:", df["trip_distance"].mean())
print("min fare amount", df['fare_amount'].min())
print("max fare aomunt", df['fare_amount'].max())
print('Avg fare amount per customers',  df.groupby('passenger_count')['fare_amount'].mean())

#print('Avg fare amount per trips from airport', df.groupby(['Airport_fee'])['fare_amount'].mean().dropna())
print('Avg fare amount per trips from airport: ', df.query('Airport_fee > 0')['fare_amount'].mean())
"""
#working awnsers

"""
print(df['tpep_pickup_datetime'])
print(type(df['tpep_pickup_datetime'].dt))
print(type(df['tpep_pickup_datetime'][0]))
df['hour_of_day'] = df['tpep_pickup_datetime'].dt.hour
df['day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek
print(df['hour_of_day'])
print(df['day_of_week'])

print('Avg congestion for each hr each day', df.groupby('hour_of_day')['congestion_surcharge'].mean())
print('Avg congestion for each day each week', df.groupby('day_of_week')['congestion_surcharge'].mean())

print('Most frequent pick up location', df['PULocationID'].value_counts().idxmax())
print('Most frequent drop off location', df['DOLocationID'].value_counts().idxmax())
print('most frequent PU/DO location pair', df.groupby(['PULocationID', 'DOLocationID']).value_counts().idxmax())
"""
#print('Most frequent PU location on weekend nights', df.

"""
Graphs:

- Trips per day
- Avg trip distance per hr of the day
- Avg fare amount per # of passangers
- Avg fare amout for trips from the airports vs. non-airport
- Avg Congetion surchage per hr of the dat; and per day of the week (grid)
- Overlay on map: most frequent pick up and drop off locations

"""

import matplotlib.pyplot as plt
### Trips per day


xy = df.groupby('date')['VendorID'].count()
x = xy.index
y = xy.values
#print(x)
#print(y)

df['week'] = df['tpep_pickup_datetime'].dt.isocalendar().week
xy_byweek = df.groupby('week')['VendorID'].count()
x_byweek = xy_byweek.index
y_byweek = xy_byweek.values
#print(x_byweek)
#print(y_byweek)

plt.plot(x, y)
plt.axvline(datetime.date(2023,11,23), color='r', linestyle='--')

# add a vertical at each Monday
for i in range(len(x)):
    if x[i].weekday() == 0:
        plt.axvline(x[i], color='g', linestyle=':')

# plot mean
plt.axhline(y.mean(), color='k', linestyle='-.')

# plot rectangle of largest week
max_week = y_byweek.argmax()
plt.axvspan(datetime.date.fromisocalendar(2023, x_byweek[max_week], 1), datetime.date.fromisocalendar(2023, x_byweek[max_week], 7), alpha=0.3, color='y')
plt.xlabel('Date')
plt.ylabel('Trips')
plt.title('Trips per day')
plt.xticks(rotation=45)
plt.ylim(0, y.max() + 100000)

# vertical line at thanksgiving
plt.tight_layout()
plt.savefig('trips_per_day.png')


###- Avg trip distance per hr of the day
hr = df['hour_of_day']
xy = df.groupby('hour_of_day')['trip_distance'].mean()
#print(xy)
x = xy.index + 1
y = xy.values
#print(x)
#print(y)

plt.clf()
plt.bar(x,y)

plt.xlabel('hour of day')
plt.ylabel('Avg Distance')
plt.xticks(range(1, 25, 2), labels=range(1, 25, 2))
plt.ylim(0, y.max() + 1)
plt.title('Avg Trip Distantce per hr')
plt.savefig('avg_trip_distance_hr.png')


###- Avg fare amount per # of passangers
df_clean = df.dropna(subset=['passenger_count', 'fare_amount'])
xy = df_clean.groupby('passenger_count')['fare_amount'].mean()
#print(xy)
x = xy.index + 1
y = xy.values
#print(x)
#print(y)




plt.clf()
plt.plot(x,y)

plt.xlabel('# of Passengers')
plt.ylabel('Avg Fare Amount')
plt.xticks(range(1, 11), labels=range(1,11))
plt.title('Avg Fare Amount per Passangers')
plt.savefig('Avg_fare_per_passangers.png')

###- Avg fare amout for trips from the airports vs. non-airport
print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
df['airport_pickup'] = df['Airport_fee'] > 0
airport_fare = df.query('airport_pickup')['fare_amount'].mean()
nonairport_fare = df.query('~airport_pickup')['fare_amount'].mean()

plt.clf()
plt.bar(['Airport', 'non-airport'], [airport_fare, nonairport_fare])

plt.title('Avg Fare Amount trips Airport vs. Non-airport')
plt.xlabel('location')
plt.ylabel('fare amount')
plt.tight_layout()
plt.savefig('Airport_vs_Nonairport.png')

###- Avg Congetion surchage per hr of the dat; and per day of the week (grid)

df['day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek
df['hour_of_day'] = df['tpep_pickup_datetime'].dt.hour
xy = df.groupby(['day_of_week', 'hour_of_day'])['congestion_surcharge'].mean()
print(xy)
xy = xy.unstack()
print(xy)

plt.clf()
plt.imshow(xy, cmap='viridis')
plt.colorbar()
plt.xticks(range(24), range(24))
plt.yticks(range(7), ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])
plt.xlabel('Hour of Day')
plt.ylabel('Day of Week')
plt.title('Congetion surcharge')
plt.tight_layout()
plt.savefig('Congestion_Surchage.png')

###- Overlay on map: most frequent pick up and drop off locations

plt.clf()
 
