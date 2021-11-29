"""
This module is deputed to the creation of graphs and charts.
It requires the installation of an external module through:

    conda install -c conda-forge mplfinance
-----------------------------------------------------------------------------------------------
"""

from matplotlib import rcParams as rc, pyplot as plt
import mplfinance as mpf
import numpy as np

style = "Solarize_Light2"
def create_single_linear_chart(dataframe, time_period=30):
    """
    This function plots and saves locally the trend of the cryptocurrency daily opening price and the graphical correlation between currency price and market capitalization in two subplots.

    INPUT PARAMETERS
        - Dataframe (as a dictionary),
        - The time window (optional. Default = 30).
    -----------------------------------------------------------------------------------------------
    """

    df = dataframe["df"]
    from_currency = dataframe["from_currency"]
    to_currency = dataframe["to_currency"]

    with plt.style.context(style):
        fig = plt.figure(figsize = (10,10))
        fig.suptitle("Single Cryptocurrency Trend", x=0.5, y=1, fontsize=35, color="#2b1fef")
        axes = fig.subplots(nrows=2, ncols=1)

        axes[0].plot(df.loc[:,"Open"][0:time_period], label = from_currency)
        axes[0].set_title(f"Last {time_period} days price trend")
        axes[0].set_xlabel("Day", fontsize = 15, fontweight = "bold")
        axes[0].set_ylabel(f"Price ({to_currency})", fontsize = 15, fontweight = "bold")
        axes[0].legend()

        axes[1].plot(df.loc[:,"High"][0:90], label = f"{from_currency} price")
        axes[1].plot(df.loc[:,"Volume"][0:90], label = f"{from_currency} Market Cap", linestyle=":")
        axes[1].set_title(f"Correlation between value and market capitalization of {from_currency}")
        axes[1].set_xlabel("Day", fontsize = 15, fontweight = "bold")
        axes[1].set_ylabel(f"Price ({to_currency})", fontsize = 15, fontweight = "bold")
        axes[1].legend()

        fig.tight_layout(pad=2.0)

        plt.savefig(f"{from_currency}_to_{to_currency}_trend.png", dpi=300)
    return None

def create_multiple_linear_chart(dataframes, time_period=30):
    """
    This function plots and saves locally the trend of the cryptocurrencies daily opening price in the same subplot.

    INPUT PARAMETERS
        - List of Dataframe (as a dictionary),
        - The time window (optional. Default = 30).
    -----------------------------------------------------------------------------------------------
    """

    with plt.style.context(style):
        fig = plt.figure(figsize = (10,10))
        fig.suptitle("Multiple Cryptocurrency Trend", x=0.5, y=1, fontsize=35, color="#2b1fef")
        axes = fig.subplots(nrows=1, ncols=1)
        
        for dataframe in dataframes:
            df = dataframe["df"]
            from_currency = dataframe["from_currency"]
            to_currency = dataframe["to_currency"]
            
            axes.plot(df.loc[:,"Open"][0:time_period], label = from_currency)

        axes.set_title(f"Last {time_period} days price trend")
        axes.set_xlabel("Day", fontsize = 15, fontweight = "bold")
        axes.set_ylabel(f"Price ({to_currency})", fontsize = 15, fontweight = "bold")
        axes.legend()

        fig.tight_layout(pad=2.0)
        plt.savefig("multi_curr_trend.png", dpi=300)
    return None

def create_candle_chart(dataframe, time_period=30):
    """
    This function plots and saves locally the daily candlestick chart of the cryptocurrency (openings, closings and shadows).

    INPUT PARAMETERS
        - Dataframe (as a dictionary),
        - The time window (optional. Default = 30).
    -----------------------------------------------------------------------------------------------
    """

    df = dataframe["df"]
    from_currency = dataframe["from_currency"]
    to_currency = dataframe["to_currency"]

    market_style = mpf.make_marketcolors(
                            up="tab:red",down="tab:green",
                            wick={"up":"red","down":"green"}
                           )

    base_style  = mpf.make_mpf_style(base_mpl_style=style, marketcolors=market_style)
    mpf.plot(df[0:time_period],
                        type = "candle", style=base_style,
                        title = f"Candlestick chart of {from_currency} for the last {time_period} days",
                        ylabel = f"Price ({to_currency})",
                        volume = True,
                        mav = 2,
                        figratio=(12,6),
                        figscale=1.5,
                        datetime_format="%d-%m-%Y",
                        savefig=f"{from_currency}_to_{to_currency}_candlestick.png")
    return None

def create_frequency_chart(dataframe, time_period=30):
    """
    This function plots and saves locally the price fluctuation over time.

    INPUT PARAMETERS
        - Dataframe (as a dictionary),
        - The time window (optional. Default = 30).
    -----------------------------------------------------------------------------------------------
    """

    df = dataframe["df"]
    from_currency = dataframe["from_currency"]
    to_currency = dataframe["to_currency"]

    with plt.style.context(style):
        fig = plt.figure(figsize = (10,10))
        fig.suptitle(f"{from_currency} price fluctuation", x=0.5, y=1, fontsize=35, color="#2b1fef")
        axes = fig.subplots(nrows=1, ncols=1)

        x = np.array(df.loc[:,["High", "Low"]].mean(axis=1))[0:time_period]
        axes.hist(x, label = from_currency, bins=15)

        axes.set_title(f"Last {time_period} days price volatility")
        axes.set_xlabel(f"Price ({to_currency})", fontsize = 15, fontweight = "bold")
        axes.set_ylabel("Volatility (n. of days)", fontsize = 15, fontweight = "bold")
        axes.legend()

        fig.tight_layout(pad=2.0)

        plt.savefig(f"{from_currency}_price_fluctuation.png", dpi=300)
    return None