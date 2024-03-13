from pyspark import SparkConf, SparkContext
import pyspark.pandas as ps
import pandas as pd
import numpy as np

conf = SparkConf()
#conf.setMaster("spark://10.80.23.119:7077")
conf.setAppName("nyctaxi")
conf.set("spark.executor.memory", "2g")
conf.set("spark.executor.cores", "1")
conf.set("spark.driver.memory", "8g")
conf.set("spark.driver.cores", "5")
spark = SparkContext(conf=conf)

df = ps.read_parquet("/data/nyctaxi/set1/*.parquet")
print(df.columns)
print(df.info(verbose=True))

#print(df['tpep_pickup_datetime'])
#print(type(df['tpep_pickup_datetime'].dt))
#print(type(df['tpep_pickup_datetime'][0]))
#df['hour_of_day'] = df['tpep_pickup_datetime'].dt.hour
#df['day_of_week'] = df['tpep_pickup_datetime'].dt.dayofweek
#print(df['hour_of_day'])
#print(df['day_of_week'])

#mean = df['fare_amount'].mean()
#print(mean)

print(df.groupby('payment_type')['fare_amount'].mean())

#Average ratio of trip cost that is tolls
# Total num of trips per month across all years
# Average prie per mile, exluding tolls and mta taxes
# Most popular pickup/dropoff locations ( use lat/long t rounded to 3 decimal places)


print(df.groupby('trip_distance')['fare_amount'].mean())
