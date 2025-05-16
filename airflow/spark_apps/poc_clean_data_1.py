import sys
import argparse

from pyspark.sql import SparkSession

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

spark = (
    SparkSession
        .builder
        .appName('POC Clean data 1')
        .getOrCreate()
)