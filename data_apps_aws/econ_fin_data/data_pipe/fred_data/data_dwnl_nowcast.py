import os

import pandas as pd
from fredapi import Fred
import numpy as np

from data_apps_aws.src.passwords import get_api_token
from data_apps_aws.src.sql import get_db_engine, overwrite_db_table_from_df

def dwnload_alfred_all_releases(ticker_list):

    # set up connection to FRED with API key
    fred = Fred(api_key=get_api_token('fred'))

    all_ticker_release_list = []

    for this_ticker in ticker_list:
        this_df = fred.get_series_all_releases(this_ticker)
        this_df['ticker'] = this_ticker

        all_ticker_release_list.append(this_df)

    all_ticker_release_data = pd.concat(all_ticker_release_list, axis=0)

    # convert NaT to nan
    xx_inds = all_ticker_release_data['value'].isna()
    all_ticker_release_data.loc[xx_inds, 'value'] = np.nan

    # convert object to float
    all_ticker_release_data['value'] = all_ticker_release_data['value'].astype(np.float)

    return all_ticker_release_data

def get_nowcast_ticker_list():

    ticker_list = ['PAYEMS', 'JTSJOL', 'CPIAUCSL', 'DGORDER', 'HSN1F', 'RSAFS', 'UNRATE', 'HOUST',
                   'INDPRO', 'PPIFIS', 'DSPIC96', 'BOPTEXP', 'BOPTIMP', 'WHLSLRIMSA', 'TTLCONS',
                   'IR', 'CPILFESL', 'PCEPILFE', 'PCEPI', 'PERMIT', 'TCU', 'BUSINV', 'IQ',
                   'GACDISA066MSFRBNY', 'PCEC96', 'GACDFSA066MSFRBPHI', 'GDPC1', 'ULCNFB', 'A261RX1Q020SBEA']

    return ticker_list

def update_full_nowcast_data():

    db_engine = get_db_engine('econ_data')

    ticker_list = get_nowcast_ticker_list()

    # download data
    all_ticker_release_data = dwnload_alfred_all_releases(ticker_list)

    # upload to database
    overwrite_db_table_from_df(all_ticker_release_data, 'archival_data', db_engine, index=False)


if __name__ == '__main__':
    update_full_nowcast_data()
