import os
import pandas as pd
from fredapi import Fred
import numpy as np

from data_apps_aws.passwords import get_api_token
from data_apps_aws.sql import get_db_engine, overwrite_db_table_from_df
from data_apps_aws.src_data_pipes.fred_config import get_nowcast_ticker_list, get_all_fred_ticker

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


def update_full_nowcast_data():

    db_engine = get_db_engine('econ_data')

    ticker_list = get_nowcast_ticker_list()

    # download data
    all_ticker_release_data = dwnload_alfred_all_releases(ticker_list)

    # upload to database
    overwrite_db_table_from_df(all_ticker_release_data, 'archival_data', db_engine, index=False)


def update_full_metadata():

    ticker_list = get_all_fred_ticker()

    # set up connection to FRED with API key
    fred = Fred(api_key=get_api_token('fred'))

    all_ticker_info_list = []

    for this_ticker in ticker_list:
        this_df = fred.get_series_info(this_ticker)

        all_ticker_info_list.append(this_df)

    all_ticker_info_df = pd.concat(all_ticker_info_list, axis=1).T

    all_ticker_info_df.rename({'id': 'ticker'}, axis=1, inplace=True)

    all_ticker_info_df['realtime_start'] = pd.to_datetime(all_ticker_info_df['realtime_start'])
    all_ticker_info_df['realtime_end'] = pd.to_datetime(all_ticker_info_df['realtime_end'])
    all_ticker_info_df['observation_start'] = pd.to_datetime(all_ticker_info_df['observation_start'])
    all_ticker_info_df['observation_end'] = pd.to_datetime(all_ticker_info_df['observation_end'])

    all_ticker_info_df['last_updated'] = pd.to_datetime(all_ticker_info_df['last_updated'], utc=True)

    # upload to database
    db_engine = get_db_engine('econ_data')

    overwrite_db_table_from_df(all_ticker_info_df, 'fred_metadata', db_engine, index=False)

