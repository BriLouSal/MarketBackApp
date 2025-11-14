
from sklearn.feature_extraction.text  import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json



from anthropic import AnthropicVertex
from anthropic import Anthropic

import os
import torch
from dotenv import load_dotenv


from yahooquery import Ticker
import pandas as pd
from MSOAI import (
    NewsSummary,
    info_to_positivty_rating_positivety,
    info_to_positivty_rating_negative,
    info_to_positivty_rating_netural,
    news,
)

load_dotenv()




def generate_universal_dataset():
    """Generate one dataset for all stocks using fictional company data."""
    dataset = {
        "Positive": info_to_positivty_rating_positivety(),
        "Neutral":  info_to_positivty_rating_netural(),
        "Negative": info_to_positivty_rating_negative()
    }

    with open('sentiment_dataset_of_stocks.json', "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=4)
