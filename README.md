# synthmind-de-assignment
Thailand stock web scraping &amp; LLM-based analysis

# Prerequisite
- docker compose

# 1 Airflow
1.1 Setup Airflow & Spark
```bash
# Do this only once.
cd airflow
docker compose build
docker compose up airflow-init # If "WARNING!!!" occured, Please set Memory limit of Docker Resources to at least 5 GB
```

1.2 Start Airflow & Spark
```bash
# Open new Terminal #1
# Keep this running forever.
cd airflow
docker compose up
```

1.3 Spark test running hello_world
```bash
# Open new Terminal #2
./script/spark_submit.sh hello_world.py
# +---+-------+
# | id|message|
# +---+-------+
# |  1|  Hello|
# |  2|  World|
# +---+-------+
```

1.4 (optional) Open jupyter notebook (localhost:8888) to check some of my POC scripts.
```bash
# Open new Terminal #3
# Keep this running forever.
./script/start_notebook.sh
# then go to the "apps" directory
```

# 2 UI
2.1 Spark UI
  - http://localhost:8080

2.2 Airflow UI
  - http://localhost:8081 (user: airflow, pass: airflow)

# 3 The procedure
![Airflow 1](/img/airflow-1.png)
1. Scrape data from 4 public sources.\
  1.1 Keep raw response status and body.\
  1.2 Organize json keys.\
  1.3 Convert to CSV.
2. Clean data using Spark.
3. Finish sentiment analysis using Transformers from Hugging Face. (3 models in English, 1 model in Thai)
4. Finish key topics extraction using Transformers from Hugging Face. (1 model in English)

![EN Sentiment](/img/en-sentiment.png)
![TH Sentiment](/img/th-sentiment.png)
![EN Key topics](/img/en-key-topics.png)

# 4 Results
![Airflow 2](/img/airflow-2.png)
### The result data produced by me can be found in the file named "result_data.zip"
### Data file structure (will be stored in airflow/ directory after finished running the DAGs)
![Data file structure](/img/data-file-structure.png)
