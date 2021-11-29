"""
This module contains the main statistical functions of Pandas:
    - variation
    - ath
    - correlation
-----------------------------------------------------------------------------------------------
"""

import numpy as np, pandas as pd
from datetime import datetime
from IPython.display import display

def variation(dataframes):
    """
    Note. Currently, this functions only works for a Daily-based Analysis.

    INPUT PARAMETERS
        - A list of Dataframes (as a Dictionary).
        
    OUTPUT PARAMETERS
        - The percentage variation of prices in a new dataframe (one day, one week, one month, three month, one year).
    -----------------------------------------------------------------------------------------------
    """

    df_columns = []
    for dataframe in dataframes:
        df = dataframe["df"]
        currency = dataframe["from_currency"]
        
        var_df = {"Day (%)": [], "Week (%)": [], "Month (%)": [], "Year (%)": []}

        for time in (1, 7, 30, 365):                                    # A Series for each currency will be created
            if time == 1:
                period = "Day (%)"
            elif time == 7:
                period = "Week (%)"
            elif time == 30:
                period = "Month (%)"
            elif time == 365:
                period = "Year (%)"
            
            s_value = df.loc[:,"Close"]
            perc_var = s_value.pct_change(periods=time)[time]           # This Pandas method returns the percentage variation of two different closing (Delta: time)
            
            var_df[period] = np.round(-perc_var*100,2)

        df_columns.append(pd.Series(var_df, name=currency))             # Each Series is appended to a List
    new_df = pd.concat(df_columns, axis=1)                              # Then, the list of Series is concatenated in a DataFrame
    new_df.index.name = "Variation"
    return display(new_df)

def ath(dataframe):
    """
    INPUT PARAMETERS
        - A Dataframe (as a Dictionary).
        
    OUTPUT PARAMETERS
        - The all-time-high value recorded and the day in which the ATH was reached.
    -----------------------------------------------------------------------------------------------
    """

    df = dataframe["df"]
    currency = dataframe["from_currency"]

    max_value = df.loc[:,"High"].max()
    data_max = df[df.loc[:,"High"]==max_value].index[0].strftime("%Y-%m-%d")
    return print(f"\nThe highest value recorded for {currency} is:\t{np.round(max_value,2).astype(str).rjust(10)} €\tin {data_max}")

def correlation(dataframe):
    """
    INPUT PARAMETERS
        - A Dataframe (as a Dictionary).
        
    OUTPUT PARAMETERS
        - The correlation between the price of a currency and his market capitalization.
    -----------------------------------------------------------------------------------------------
    """

    df = dataframe["df"]
    currency = dataframe["from_currency"]

    s1 = df.loc[:,["Open", "Close"]].aggregate(func="mean", axis=1)
    s2 = df.loc[:,"Volume"]
    corr = np.round(s1.corr(s2), 3)

    if corr < 0.3:
        corr_result = f"NO correlation between value and market capitalization of "
    elif corr < 0.6:
        corr_result = f"a MEDIUM correlation between value and market capitalization of "
    elif corr < 0.9:
        corr_result = f"a STRONG correlation between value and market capitalization of "
    else:
        corr_result = f"a FULL correlation between value and market capitalization of "
    
    return print(f"\nThere is {corr_result}{currency}:\t{corr}")

def disp(dataframe):
    """
    This function was made to display correctly the DataFrame.

    INPUT PARAMETERS
        - A Dataframe (as a Dictionary).
        
    OUTPUT PARAMETERS
        - The Dataframe.
    -----------------------------------------------------------------------------------------------
    """

    df = dataframe["df"]
    return display(df)

def stat_func(dataframe):
    """
    This functions returns the Median, Mean and Deviation Standard for opening price for the selected currency

    INPUT PARAMETERS
        - Dataframe (as a Dictionary)

    OUTPUT PARAMETERS
        - Statistical parameters (Median, Mean and Deviation Standard)
        - Mean price value over years
    """

    df = dataframe["df"]
    currency = dataframe["from_currency"]

    print(f"\nMain statistical parameters for {currency} opening values")
    display(df["Open"].aggregate(func=["median", "mean", "std"]).to_frame())

    print(f"\nMean {currency} price year over years has been:")
    display(df["Open"].groupby([df.index.year]).mean())
    return None