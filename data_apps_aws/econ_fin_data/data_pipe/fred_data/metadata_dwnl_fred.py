import pandas as pd
from fredapi import Fred

from data_apps_aws.src.passwords import get_api_token
from data_apps_aws.src.sql import get_db_engine, overwrite_db_table_from_df

from data_apps_aws.econ_fin_data.data_pipe.fred_data.data_dwnl_nowcast import get_nowcast_ticker_list


def get_all_fred_ticker():

    return get_nowcast_ticker_list()


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


if __name__ == '__main__':

    update_full_metadata()

