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

# tabularisai/multilingual-sentiment-analysis
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ahmedrachid/FinancialBERT-Sentiment-Analysis
from transformers import BertTokenizer, BertForSequenceClassification

# mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis
from transformers import RobertaTokenizer, AutoModelForSequenceClassification


parser = argparse.ArgumentParser()
parser.add_argument('thisfile') 
parser.add_argument("-d", "--date", help="execution date.")
args = parser.parse_args()

if args.date:
    execution_date = args.date

print('execution_date')
print(execution_date)

login(token='xxx')

read_paths  = [
    f'./data/4_clean_news/03_seten/{execution_date}',
    f'./data/4_clean_news/04_kaohoon/{execution_date}',
]
write_dir  = f'./data/5_sentiment/01_en/{execution_date}'
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

df.to_csv(write_path, index=False, mode='w')

exit(0)

# ===
# Model #1
# ===
model_name = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def predict_sentiment_1(texts):
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
    
    sentiment_map = {0: "negative", 1: "negative", 2: "neutral", 3: "positive", 4: "positive"}
    return [sentiment_map[p] for p in torch.argmax(probabilities, dim=-1).tolist()][0]

df['sentiment_1'] = df['news_text'].apply(predict_sentiment_1)
print(df.head())

# ===
# Model #2
# ===
model = BertForSequenceClassification.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis", num_labels=3)
tokenizer = BertTokenizer.from_pretrained("ahmedrachid/FinancialBERT-Sentiment-Analysis")
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def predict_sentiment_2(text):
    result = nlp(text[:512])[0]  # truncate to max length if needed
    return result['label']

df['sentiment_2'] = df['news_text'].apply(predict_sentiment_2)
print(df.head())

# ===
# Model #3
# ===
model = AutoModelForSequenceClassification.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis", num_labels=3)
tokenizer = RobertaTokenizer.from_pretrained("mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis")
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

def predict_sentiment_3(text):
    result = nlp(text[:512])[0]  # truncate to max length if needed
    return result['label']

df['sentiment_3'] = df['news_text'].apply(predict_sentiment_3)
print(df.head())

# ===
# Combined results of 3 models
# ===
# if tie, get final result from Model #3
def majority_bias3(row):
    score = {"negative": 0, "neutral": 0, "positive": 0}
    score[row['sentiment_1']] += 1
    score[row['sentiment_2']] += 1
    score[row['sentiment_3']] += 1

    score_max = max(score, key=score.get)
    score_min = min(score, key=score.get)

    if score_max == score_min:
        score_max = row['sentiment_3'] # if tie, get final result from Model #3

    return score_max

df['sentiment_final'] = df.apply(majority_bias3, axis=1)
df = df.drop('news_text', axis=1)
print(df.head())

df.to_csv(write_path, index=False, mode='w')