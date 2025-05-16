import sys
import argparse

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, 
    substring,
    lit,
    trim,
    replace,
    translate
)

print('sys.argv')
print(sys.argv)

parser = argparse.ArgumentParser()
parser.add_argument('thisfile') 
parser.add_argument("-d", "--date", help="execution date.")
args = parser.parse_args()

if args.date:
    execution_date = args.date

print('execution_date')
print(execution_date)

read_path  = f'./data/3_raw_news/02_infoquest/{execution_date}'
write_path = f'./data/4_clean_news/02_infoquest/{execution_date}'

spark = (
    SparkSession
        .builder
        .appName('POC Clean data 2')
        .getOrCreate()
)

df = spark.read.options(header=True, multiLine=True, escape='"').csv(read_path)
df2 = df \
 .withColumn('news_datetime',  substring('news_datetime', 1, 10)) \
 .withColumn('news_content',   trim(translate('news_content', '\n', ' '))) \
 .withColumn('news agency',    lit('infoquest')) \
 .withColumn('execution_date', lit(execution_date))

df2.write.mode("overwrite").options(header=True, multiLine=True, escape='"').csv(write_path)