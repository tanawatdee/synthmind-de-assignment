import sys
import argparse
from datetime import datetime

# for sentimental analysis
import os
import glob
import pandas as pd
from torch.nn.functional import softmax
import torch
from huggingface_hub import login

from transformers import (
    TokenClassificationPipeline,
    AutoModelForTokenClassification,
    AutoTokenizer,
)
from transformers.pipelines import AggregationStrategy
import numpy as np


parser = argparse.ArgumentParser()
parser.add_argument('thisfile') 
parser.add_argument("-d", "--date", help="execution date.")
args = parser.parse_args()

if args.date:
    execution_date = args.date

print('execution_date')
print(execution_date)

login(token='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')

read_path  = f'./data/5_sentiment/01_en/{execution_date}'
write_dir  = f'./data/6_key_topics/01_en/{execution_date}'
write_path = f'{write_dir}/00000.csv'

if not os.path.isdir(write_dir):
    os.makedirs(write_dir)

csv_files = glob.glob(read_path + "/*.csv")
df_list = (pd.read_csv(file) for file in csv_files)
df = pd.concat(df_list, ignore_index=True)
df['news_text'] = df['news_content'].fillna('') + ' ' + df['news_title']

print(df.head())

# Define keyphrase extraction pipeline
class KeyphraseExtractionPipeline(TokenClassificationPipeline):
    def __init__(self, model, *args, **kwargs):
        super().__init__(
            model=AutoModelForTokenClassification.from_pretrained(model),
            tokenizer=AutoTokenizer.from_pretrained(model),
            *args,
            **kwargs
        )

    def postprocess(self, all_outputs):
        results = super().postprocess(
            all_outputs=all_outputs,
            aggregation_strategy=AggregationStrategy.SIMPLE,
        )
        return np.unique([result.get("word").strip() for result in results])
    
# Load pipeline
model_name = "ml6team/keyphrase-extraction-kbir-inspec"
extractor = KeyphraseExtractionPipeline(model=model_name)

def predict_key_topics(text):
    print('news_text')
    print(text)

    news_key_topics = extractor(text)

    print('news_key_topics')
    print(news_key_topics)
    print('')

    return news_key_topics

df['news_key_topics'] = df['news_text'].apply(predict_key_topics)
print(df.head())

df.to_csv(write_path, index=False, mode='w')