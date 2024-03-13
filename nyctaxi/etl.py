from pyspark import SparkConf, SparkContext
import pandas as pd
import pyspark.pandas as ps
import os
import glob


#per parquest file, load, extract certain columns
#save as new parquet file in your home dir
#analysis.py
#Readme.md desc. of of dataset etl steps analysis
#including images


conf = SparkConf()
spark = SparkContext(conf=conf)

for f in glob.glob("/data/nyctaxi/set1/*.parquet"):
	print("NEW FILE READING~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	print(f)
	df = ps.read_parquet(f)
	print("columns: ", df.columns)
	print("info:")
	print(df.info(verbose=True))

	select = ["fare_amount", "total_amount", "passenger_count"]
	df_select = df[select]
	output_dir = os.path.expanduser("/home/orgonzales/files/")
	os.makedirs(output_dir, exist_ok=True)
	output_path = os.path.join(output_dir, os.path.basename(f))

	df_select.to_parquet(output_path)
	print("file saved in : ", output_path)

#df = ps.read_parquet("/data/nyctaxi/set1/*.parquet")
#print(df.columns)

sc.stop()

