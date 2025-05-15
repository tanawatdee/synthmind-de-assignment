import os
from datetime import datetime as dt

from pyspark.sql import SparkSession

spark = (
    SparkSession
        .builder
        .appName('Hello World')
        .getOrCreate()
)

df = spark.createDataFrame([(1, "Hello"), (2, "World")], ["id", "message"])
df.show()