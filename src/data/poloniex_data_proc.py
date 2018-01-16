import pandas as pd


def get_historical_data_from_file(base_currency, other_currency, frequency, start_date, end_date):
       root_folder = '/Users/Eamon/Dropbox/Logistio/Software/Python_Programmes'
       data_folder = 'cryptocurrency.backtester/data/01.01.2017-12.01.2018'
       file_prefix = 'RAW'
       file_name = '_'.join([file_prefix, base_currency, other_currency]) + '.csv'
       extension = '.csv'

       #full_file_name = '/'.join([root_folder, data_folder, file_name])
       full_file_name = '/'.join(['/crypto-backtest/data/01.01.2017-12.01.2018', file_name])
       cols = ['index', 'type', 'rate', 'volume']

       df = pd.read_csv(full_file_name, names=cols, index_col=0, parse_dates=True)
       df = df['rate'].resample(frequency).ohlc().fillna(method='ffill')
       df['quoteVolume'] = ''
       df['volume'] = ''
       df['weightedAverage'] = ''
       df = df[start_date : end_date]
       return df


# frequency = '1Min'
# base_currency = 'BTC'
# other_currency = 'AMP'
# start_date = '2017-01-01 00:24:00'
# end_date = '2017-01-01 00:28:00'
#
# df = get_historical_data_from_file(base_currency, other_currency, frequency, start_date, end_date)
# print(df.head())