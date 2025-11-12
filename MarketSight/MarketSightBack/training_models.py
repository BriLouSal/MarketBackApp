
from sklearn.feature_extraction.text  import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split


from anthropic import AnthropicVertex
from anthropic import Anthropic

import os
from dotenv import load_dotenv


from yahooquery import Ticker
import pandas as pd
from .MSOAI import NewsSummary, info_to_positivty_rating_positivety, info_to_positivty_rating_negative, info_to_positivty_rating_netural

load_dotenv()


# API KEYS:

CLAUDE_API = os.getenv('CLAUDE')

client = Anthropic(api_key=CLAUDE_API)





# Check positivety for news
def positivity_rating(stock: str):
    """
  Description:
  Use Claude API to generate a messages of financial report that has 
    """
    # Data to use:
    positive_data =  info_to_positivty_rating_positivety(stock=stock.upper())
    negative_data = info_to_positivty_rating_negative(stock=stock.upper())
    netural_data = info_to_positivty_rating_netural(stock=stock.upper())
    
    if not positive_data or negative_data:
        raise ValueError(f"No data found for f{stock}")
    
    model = pd.DataFrame({
        'text': positive_data + negative_data + netural_data
    })



    
    main_data = TfidfVectorizer(max_features=1000)

    



    





























