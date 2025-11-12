
from sklearn.feature_extraction.text  import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


from anthropic import AnthropicVertex
from anthropic import Anthropic

import os
from dotenv import load_dotenv


from yahooquery import Ticker
import pandas as pd
from .MSOAI import NewsSummary, info_to_positivty_rating_positivety, info_to_positivty_rating_negative, info_to_positivty_rating_netural, news

load_dotenv()


# API KEYS:

CLAUDE_API = os.getenv('CLAUDE')

client = Anthropic(api_key=CLAUDE_API)



def check_language(news: str):
    pass

# Check positivety for news, train the data
def positivity_rating_training(stock: str):
    """
  Description:
  Use Claude API to generate a messages of financial report that has 
    """
    # Data to use:
    positive_data =  info_to_positivty_rating_positivety(stock=stock.upper())
    negative_data = info_to_positivty_rating_negative(stock=stock.upper())
    netural_data = info_to_positivty_rating_netural(stock=stock.upper())
    
    # If not data for either of the stock
    if not positive_data or not negative_data or not netural_data:
        raise ValueError(f"No data found for f{stock}")
    
    model = pd.DataFrame({
        'text': positive_data + negative_data + netural_data,
        'label': [2] * len(positive_data) + [1] * len(negative_data) + [0] * len(netural_data),
    })
    
    # Vectorizer, considers importance of the words
        
    main_data = TfidfVectorizer(max_features=1000)


    X = main_data.fit_transform(model['text'])
    y = model['label']

    # Test

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Use Logistic Regression to predict the positivity rating,
    # This will be our training dataset, and we're using Claude API to get those positive
    # words for stocks, and then we'll compare it after
    model_of_data = LogisticRegression()
    model_of_data.fit(X_test, y_test)

    accuracy = model_of_data.score(X_test, y_test)

    return model_of_data, main_data



def obtain_positivity(stock: str, models_of_data, main_data) -> dict:
    news_of_stock = news(stock=stock.upper())

    if not news_of_stock:
        return None, "No News is available"
    
