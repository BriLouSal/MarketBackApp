import pandas as pd
import yfinance as yf
from tqdm import tqdm
from ta.momentum import RSIIndicator
from ta.trend import SMAIndicator
from ta.volatility import BollingerBands





def get_asset_info(self, df=None):
        """
        Description:
        Grabs historical prices for assets, calculates RSI and Bollinger Bands tech signals, and returns a df with all this data for the assets meeting the buy criteria.
        Argument(s):
            • df: a df can be provided to specify which assets you'd like info for since this method is used in the Alpaca class. If no df argument is passed then tickers from get_trading_opportunities() method are used.
        """

        # Grab technical stock info:
        if df is None:
            all_tickers = self.all_tickers
        else:
            all_tickers = list(df["yf_ticker"])

        df_tech = []
        for i, symbol in tqdm(
            enumerate(all_tickers),
            desc="• Grabbing technical metrics for "
            + str(len(all_tickers))
            + " assets",
        ):
            try:
                Ticker = yf.Ticker(symbol)
                Hist = Ticker.history(period="1y", interval="1d")

                for n in [14, 30, 50, 200]:
                    # Initialize MA Indicator
                    Hist["ma" + str(n)] = sma_indicator(
                        close=Hist["Close"], window=n, fillna=False
                    )
                    # Initialize RSI Indicator
                    Hist["rsi" + str(n)] = RSIIndicator(
                        close=Hist["Close"], window=n
                    ).rsi()
                    # Initialize Hi BB Indicator
                    Hist["bbhi" + str(n)] = BollingerBands(
                        close=Hist["Close"], window=n, window_dev=2
                    ).bollinger_hband_indicator()
                    # Initialize Lo BB Indicator
                    Hist["bblo" + str(n)] = BollingerBands(
                        close=Hist["Close"], window=n, window_dev=2
                    ).bollinger_lband_indicator()

                df_tech_temp = Hist.iloc[-1:, -16:].reset_index(drop=True)
                df_tech_temp.insert(0, "Symbol", Ticker.ticker)
                df_tech.append(df_tech_temp)
            except:
                KeyError
            pass

        df_tech = [x for x in df_tech if not x.empty]
        df_tech = pd.concat(df_tech)

        # Define the buy criteria
        buy_criteria = (
            (df_tech[["bblo14", "bblo30", "bblo50", "bblo200"]] == 1).any(axis=1)
        ) | ((df_tech[["rsi14", "rsi30", "rsi50", "rsi200"]] <= 30).any(axis=1))

        # Filter the DataFrame
        buy_filtered_df = df_tech[buy_criteria]

        # Create a list of tickers to trade
        self.buy_tickers = list(buy_filtered_df["Symbol"])

        return buy_filtered_df


def get_losers(self):
     pass