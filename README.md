# synthmind-de-assignment
Thailand stock web scraping &amp; LLM-based analysis

# Prerequisite
- docker compose

# Setup spark
```bash
cd spark-cluster
docker compose build
```

# Start Spark cluster 
```bash
cd spark-cluster
docker compose up
```

# Spark test running hello-world
```bash
./script/spark_submit.sh hello-world.py
# +---+-------+
# | id|message|
# +---+-------+
# |  1|  Hello|
# |  2|  World|
# +---+-------+
```