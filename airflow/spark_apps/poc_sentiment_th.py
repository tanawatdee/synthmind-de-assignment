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

# all models
from transformers import pipeline

# phoner45/wangchan-sentiment-thai-text-model
from transformers import AutoTokenizer, AutoModelForSequenceClassification


parser = argparse.ArgumentParser()
parser.add_argument('thisfile') 
parser.add_argument("-d", "--date", help="execution date.")
args = parser.parse_args()

if args.date:
    execution_date = args.date

print('execution_date')
print(execution_date)

login(token='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')

read_paths  = [
    f'./data/4_clean_news/01_set/{execution_date}',
    f'./data/4_clean_news/02_infoquest/{execution_date}',
]
write_dir  = f'./data/5_sentiment/02_th/{execution_date}'
write_path = f'{write_dir}/00000.csv'

if not os.path.isdir(write_dir):
    os.makedirs(write_dir)

csv_files = []
for read_path in read_paths:
    csv_files.extend(glob.glob(read_path + "/*.csv"))

df_list = (pd.read_csv(file) for file in csv_files)

df = pd.concat(df_list, ignore_index=True)
df['news_text'] = df['news_content'].fillna('') + ' ' + df['news_title']

print(df.head())

# ===
# Model #1
# ===
model_name = "phoner45/wangchan-sentiment-thai-text-model"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Sentiment labels
labels = ['negative', 'neutral', 'positive']

# Predict function
def predict_sentiment_1(text):
    inputs = tokenizer(text[:512], return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = softmax(outputs.logits, dim=1)
    label_index = torch.argmax(probs).item()
    return labels[label_index]

df['sentiment_final'] = df['news_text'].apply(predict_sentiment_1)
print(df.head())

df.to_csv(write_path, index=False, mode='w')