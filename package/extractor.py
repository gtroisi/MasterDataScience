"""
This module is deputed to the creation of a DataFrame by means of the "create_df" function.
It also reads two files containing some parameters for the analysis:
    - const-init.json           This file contains the API key and the type of analysis to be made (DAILY, WEEKLY, MONTHLY - Default: DAILY),
    - symbol_list.csv           This file contains a list of all the accepted currency by the Server.
-----------------------------------------------------------------------------------------------
"""

import json, csv, pandas as pd
from urllib.request import urlopen
import sys

init_path = "const-init.json"
symbol_path = "symbol_list.csv"

with open(init_path) as file:
    read = json.load(file)
    API_KEY = read["api-key"]
    FUNC = read["extraction-type"]
    TIME_SERIES = read["time-heading"]

with open(symbol_path) as file:
    symbols = [row["SYMBOLS"] for row in csv.DictReader(file)]


class APICryptoClient:
    """
    The inizialization of this class creates the url object needed for the request to AlphaVantage API.

    INPUT PARAMETERS
        - Two currencies for the conversion.
    -----------------------------------------------------------------------------------------------
    """

    def __init__(self, from_symbol, to_symbol):
        if from_symbol not in symbols:
            raise ValueError(f"{from_symbol} is NOT a valid symbol. Look at \"symbol_list.csv\" attached file.")

        elif to_symbol not in symbols:
            raise ValueError(f"{to_symbol} is NOT a valid symbol. Look at \"symbol_list.csv\" attached file.")

        else:
            self.url = f"https://www.alphavantage.co/query?function={FUNC}&symbol={from_symbol}&market={to_symbol}&apikey={API_KEY}"
            self.from_symbol = from_symbol
            self.to_symbol = to_symbol

    def get_data(self):
        """
        This method reads the url initialized from the class and returns a request from the Server in the form of a Json Dataset.
        -----------------------------------------------------------------------------------------------
        """

        self.request = urlopen(self.url)
        return self.request

    def convert_to_dataframe(self):
        """
        This method reads the Json file obtained from the Server and converts it to a pandas DataFrame.

        INPUT PARAMETERS
            - Json Dataset.

        OUTPUT PARAMETERS
            - DataFrame.
        -----------------------------------------------------------------------------------------------
        """

        self.js = json.load(self.request)[TIME_SERIES]                      # The Dataset from AlphaVantage includes a "Metadata" column that is redundant. Only the "TimeSeries" column is useful for the purpose of this project.
        self.df = pd.DataFrame(self.js).astype(float)
        return self.df

    def clean_dataframe(self):
        """
        This method alters the Dataframe by:
        - Deleting the unused columns,
        - Renaming the columns,
        - Inverting columns and rows,
        - Converting USD to EUR,
        - Setting an index name,
        - Converting the index type from Float to DateTime.

        INPUT PARAMETERS
            - Dataframe from Class.

        OUTPUT PARAMETERS
            - Cleaned DataFrame.
        -----------------------------------------------------------------------------------------------
        """

        self.df.drop([self.df.index[1], self.df.index[3], self.df.index[5], self.df.index[7], self.df.index[8]], inplace = True)
        self.df.set_axis(["Open", "High", "Low", "Close", "Volume"], inplace = True)
        self.df = self.df.T
        self.df["Volume"] = self.df["Volume"].apply(lambda x: x * 0.82)     # 0.82 is the exchange rate between EUR and USD
        self.df.index.name = "Date"
        self.df.index = pd.to_datetime(self.df.index)
        return self.df


def create_df(from_symbol, to_symbol):
    """
    This function creates the DataFrame by creating an APICryptoClient class object and calling all of its methods.

    INPUT PARAMETERS
        - Two currencies to be converted.
          If the currency is not accepted by the Server, a ValueError exception will be raised.

    OUTPUT PARAMETERS
        - A dictionary containing the DataFrame, the Source currency and the Destination currency.
    -----------------------------------------------------------------------------------------------
    """

    try:
        currency = APICryptoClient(from_symbol, to_symbol)
    except ValueError as err:
        return print(err)
    else:
        currency.get_data()
        currency.convert_to_dataframe()
        dict_df = {"df": currency.clean_dataframe(), "from_currency": currency.from_symbol, "to_currency": currency.to_symbol}
        return dict_df