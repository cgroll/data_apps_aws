import subprocess
import os
import glob
import shutil
import pandas as pd

import datetime
from pandas.tseries.offsets import DateOffset, MonthEnd
import dateutil.relativedelta

from data_apps_aws.sql import *

# Load the files from a date directory
def load_csv_dir(data_dir):
    return pd.concat(map(pd.read_csv, glob.glob(os.path.join(data_dir, '*.csv'))))

# %%

def get_upload_data(this_date, this_stock_exchange):

    if this_stock_exchange == 'xetra':
        this_stock_exchange_url = "s3://deutsche-boerse-xetra-pds/"

    elif this_stock_exchange == 'eurex':
        this_stock_exchange_url = "s3://deutsche-boerse-eurex-pds/"

    else:
        raise ValueError(f'Unknown stock exchange: {this_stock_exchange}')

    this_local_folder_name = f"/tmp/xetra_eurex_1_min_data/deutsche-boerse-{this_stock_exchange}-pds/{this_date}"
    this_s3_folder_name = this_stock_exchange_url + this_date

    # make local directory
    os.makedirs(this_local_folder_name, exist_ok=True)

    # download (sync) files from s3
    subprocess.run(['aws', 's3', 'sync', this_s3_folder_name, this_local_folder_name])

    # load data from disk
    raw_data = load_csv_dir(this_local_folder_name)

    # clean-up
    shutil.rmtree(this_local_folder_name)

    return raw_data

# %%

def update_data_in_db(this_date, this_stock_exchange):

    # upload to SQL
    db_con = get_db_engine('econ_data')

    obs_data_table_name = f'{this_stock_exchange}_1min_data'

    data = get_upload_data(this_date, this_stock_exchange)

    # upload_df_to_table(data, obs_data_table_name,
    #                    db_con, index=False, if_exists='append')
    overwrite_db_table_from_df_matching_single_eq_condition(data, obs_data_table_name,
                                                         db_con, 'Date', this_date, index=False)

    db_con.dispose()

# %%

def get_delayed_xetra_date_to_process():

    today = datetime.date.today()
    date_offset = today - dateutil.relativedelta.relativedelta(days=2)
    date_offset_str = date_offset.strftime('%Y-%m-%d')

    return date_offset_str



if __name__=='__main__':

    this_date = get_delayed_xetra_date_to_process()
    update_data_in_db(this_date, 'xetra')

    this_stock_exchange = 'xetra'

    if this_stock_exchange == 'xetra':
        start_date = '2017-06-17'
        start_date = '2017-09-13'
        start_date = '2020-08-21'
    elif this_stock_exchange == 'eurex':
        start_date = '2017-05-27'
    else:
        raise ValueError(f'Unknown stock exchange: {this_stock_exchange}')

    # update_data_in_db('2020-08-21', this_stock_exchange)

    datelist = pd.date_range(start=start_date, end='2020-09-01').tolist()

    # get current dates in database
    db_con = get_db_engine('econ_data')

    query = f"""
    SELECT distinct(Date) as dates
    FROM xetra_1min_data
    """
    existing_dates = get_db_data(query, db_con).squeeze()
    db_con.dispose()

    for this_date in datelist:

        this_date_str = this_date.strftime('%Y-%m-%d')
        print(this_date_str)

        if this_date_str in existing_dates.values:
            continue
        else:
            try:
                update_data_in_db(this_date_str, this_stock_exchange)

            except:
                print('Failed')
