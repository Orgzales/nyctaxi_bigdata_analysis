from pyspark import SparkConf, SparkContext
import pandas as pd
import pyspark.pandas as ps


#per parquest file, load, extract certain columns
#save as new parquet file in your home dir
#analysis.py
#Readme.md desc. of of dataset etl steps analysis
#including images


#conf = SparkConf()

for f in glob.glob("/data/nyctaxi/set1/*.parquet")
	print(f)
	df = ps.read_parquet(f)
	print(df.columns)
	print(df.info(verbose=True)


#df = ps.read_parquet("/data/nyctaxi/set1/*.parquet")
#print(df.columns)
