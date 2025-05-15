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

# 2 UI
2.1 Spark UI
  - http://localhost:8080

2.2 Airflow UI
  - http://localhost:8081 (user: airflow, pass: airflow)
