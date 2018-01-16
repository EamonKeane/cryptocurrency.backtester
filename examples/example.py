from gemini.gemini import Gemini
from gemini.helpers import poloniex as px
from gemini.helpers.analyze import analyze_mpl, analyze_bokeh
from src.data.poloniex_data_proc import get_historical_data_from_file


def logic(algo, data):
    """
    Main algorithm method, which will be called every tick.

    :param algo: Gemini object with account & positions
    :param data: History for current day
    """

    if len(data) < 2:
        # Skip short history
        return

    today = data.iloc[-1]  # Current candle
    yesterday = data.iloc[-2]  # Previous candle

    # close positions
    if len(algo.account.positions) > 0:
        if today['close'] < yesterday['close']:
            exit_price = today['close']
            for position in algo.account.positions:
                if position.type_ == 'Long':
                    algo.account.close_position(position, 1, exit_price)

    # open positions
    elif today['close'] > yesterday['close']:
        risk = 0.9
        entry_price = today['close']
        entry_capital = algo.account.buying_power * risk
        if entry_capital >= 0.00001:
            algo.account.enter_position('Long', entry_capital, entry_price)

#########
# Get data using poloniex
# Data settings
# pair = "SC_BTC"    # Use ETH pricing data on the BTC market
# period = 14400       # Use 1800 second candles
# days_history = 180  # Collect 100 days data
#
# # # Request data from Poloniex
# df = px.load_dataframe(pair, period, days_history)

######

######
# get data from file stored on disk
start_date = '2017-01-04 0:00:00'
end_date = '2017-12-31 23:59:59'
base_currency = 'BTC'
other_currency = 'XRP'
frequency = '1D'

df = get_historical_data_from_file(base_currency, other_currency, frequency, start_date, end_date)


########

# Algorithm settings
sim_params = {
    'capital_base': 10,      # initial capital in BTC
    'fee': {
        'Long': 0.0015,      # fee settings for Long
        'Short': 0.0015,     # fee settings for Short
    },
    'data_frequency': '1D'    # Time frame to use (see /helpers/timeframe_resampler.py for more info
}
gemini = Gemini(logic=logic, sim_params=sim_params, analyze=analyze_bokeh)

# start backtesting custom logic with 10 (BTC) intital capital
gemini.run(df, show_trades=True)

