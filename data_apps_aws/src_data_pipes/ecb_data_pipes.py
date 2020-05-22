import pandas as pd
import numpy as np
from pandasdmx import Request

from data_apps_aws.sql import *
from pandas.tseries.offsets import DateOffset

ecb = Request('ECB')

def get_all_resources():
    """
    Find all resources (datasets) at ECB. Return dataframe with names and dataset acronyms
    """

    flow_response = ecb.dataflow()
    resources_df = flow_response.write().dataflow

    return resources_df


def get_resource_name(this_resource_id):
    """
    Translate resource id (code) into name
    """

    resources_df = get_all_resources()
    this_resource_name = resources_df.loc[this_resource_id, 'name']

    return this_resource_name


def get_resource_metadata_decodes(this_resource_id):
    """
    Get dataframe with all codes and decodes (names) for a given resource id (dataset).
    """

    this_resource_decodes = ecb.dataflow(this_resource_id).write().codelist

    return this_resource_decodes


def get_concept_name_mapping(decodes_df):
    """

    :param decodes_df: DataFrame as obtained from get_resource_metadata_decodes
    :return: reduced DataFrame that shows all concept (metadata dimensions) codes and names
    """
    df_single_idx = decodes_df.reset_index()
    data_concepts = df_single_idx[df_single_idx['level_0'] == df_single_idx['level_1']]
    data_concepts = data_concepts.loc[:, ['level_0', 'name']]
    data_concepts.columns = ['concept_code', 'concept_name']

    return data_concepts


def get_ecb_data(resource_id, keys, params):
    """
    Download actual data, e.g.:

    get_ecb_data(this_resource_id, {'FREQ': 'M', 'PROVIDER_FM_ID': 'SOV_CI', 'DATA_TYPE_FM': 'IDX'}, {'startPeriod': '2016'})

    :param resource_id: specifies dataset
    :param keys: allows subsets according to concepts (metadata dimensions)
    :param params: additional parameters, e.g. date range
    :return: DataFrame with data
    """
    if params is None:
        data_response = ecb.data(resource_id, key=keys)
    else:
        data_response = ecb.data(resource_id, key=keys, params=params)

    # transform response to dataframe
    raw_data = data_response.data
    series_tuple = (s for s in raw_data.series)
    data = data_response.write(series_tuple)

    return data


def make_long_format(this_data):
    """
    Transform ECB data response into long-format. Needs to deal with multi-index column names. Maps them to metadata columns.
    :param this_data: DataFrame as returned by get_ecb_data
    :return: long format data
    """
    id_vars = this_data.columns.names
    return this_data.T.reset_index().melt(id_vars=id_vars).dropna()


def get_ciss_data(start_date):
    """
    CISS: Composite Indicator of Systemic Stress

    Download CISS data. Needs to deal with fact that some time series are monthly and some are daily.
    Since dates are given as TimePeriod, monthly data first needs to be transformed to be concatenated with
    daily timestamps.

    :return: DataFrame with all CISS data in long format
    """
    this_resource_id = 'CISS'

    monthly_data_countries = make_long_format(
        get_ecb_data(this_resource_id, {'FREQ': 'M', 'PROVIDER_FM_ID': 'SOV_CI', 'DATA_TYPE_FM': 'IDX'},
                     {'startPeriod': start_date}))
    monthly_data_regions = make_long_format(
        get_ecb_data(this_resource_id, {'FREQ': 'M', 'PROVIDER_FM_ID': ['SOV_EW', 'SOV_GDPW']},
                     {'startPeriod': start_date}))

    monthly_data = pd.concat([monthly_data_countries, monthly_data_regions], axis=0)
    monthly_data['TIME_PERIOD'] = pd.to_datetime([this_tp.to_timestamp(how='E').date() for this_tp in monthly_data['TIME_PERIOD']])

    daily_data_countries = make_long_format(get_ecb_data(this_resource_id, {'FREQ': 'D'}, {'startPeriod': start_date}))
    daily_data_countries['TIME_PERIOD'] = pd.to_datetime([this_tp.to_timestamp(how='E').date() for this_tp in daily_data_countries['TIME_PERIOD']])

    all_ciss_data = pd.concat([daily_data_countries, monthly_data], axis=0)

    return all_ciss_data


def get_irs_data(start_date):
    """
    IRS: Long-term interest rate statistics

    :return:
    """

    this_resource_id = 'IRS'

    # define list of EUR area / not EUR area countries
    EMU = ['AT', 'BE', 'CY', 'DE', 'ES', 'FI', 'FR', 'GR', 'IE', 'IT', 'LT', 'LU', 'LV', 'MT', 'NL', 'PT', 'SI', 'SK',
           'U2']
    not_EMU = ['BG', 'CZ', 'D0', 'DK', 'GB', 'HR', 'HU', 'PL', 'RO', 'SE']

    keys_emu = {'FREQ': 'M', 'MATURITY_CAT': 'CI', 'REF_AREA': EMU}
    int_rates_data_emu = make_long_format(get_ecb_data(this_resource_id, keys_emu, params={'startPeriod': start_date}))

    keys_not_emu = {'FREQ': 'M', 'MATURITY_CAT': 'CI', 'REF_AREA': not_EMU}
    int_rates_data_not_emu = make_long_format(get_ecb_data(this_resource_id, keys_not_emu, params={'startPeriod': start_date}))

    int_rates_data = pd.concat([int_rates_data_emu, int_rates_data_not_emu], axis=0)

    int_rates_data['TIME_PERIOD'] = pd.to_datetime([this_tp.to_timestamp(how='E').date() for this_tp in int_rates_data['TIME_PERIOD']])

    return int_rates_data


def get_yc_data(start_date):

    this_resource_id = 'YC'

    keys = {'FREQ': 'B', 'DATA_TYPE_FM': ['BETA0', 'BETA1', 'BETA2', 'BETA3', 'TAU1', 'TAU2']}
    data = make_long_format(get_ecb_data(this_resource_id, keys, params={'startPeriod': start_date}))

    data['TIME_PERIOD'] = pd.to_datetime([this_tp.to_timestamp(how='E').date() for this_tp in data['TIME_PERIOD']])

    return data

def get_metadata_lookup(this_data_df, this_decodes_df):

    # identify metadata columns
    value_col_names = ['TIME_PERIOD', 'value']
    metadata_cols = [this_col for this_col in this_data_df.columns.values if this_col not in value_col_names]

    # get list of all occurring values
    this_data_occur_metadata = this_data_df.loc[:, metadata_cols]
    this_data_occur_metadata = this_data_occur_metadata .melt().drop_duplicates()
    this_data_occur_metadata.columns = ['concept_code', 'value_code']

    # get mapping from value codes to value names
    name_mapping = this_decodes_df.reset_index().loc[:, ['level_0', 'level_1', 'name']]
    name_mapping.columns = ['concept_code', 'value_code', 'value_name']

    # get mapping from concept codes to concept names
    concept_name_mapping = get_concept_name_mapping(this_decodes_df)

    all_metadata_codes_decodes = this_data_occur_metadata.merge(concept_name_mapping).merge(name_mapping)
    all_metadata_codes_decodes = all_metadata_codes_decodes.loc[:,
                                 ['concept_code', 'concept_name', 'value_code', 'value_name']]

    return all_metadata_codes_decodes


def get_upload_data(this_resource_id, this_obs_data, this_metadata):

    # identify unique dimensions
    dimensions_per_concept = this_metadata.groupby('concept_code')['value_code'].count()
    unanimous_concepts = dimensions_per_concept[dimensions_per_concept == 1].index.values

    # drop columns with unique dimension and add resource_id column
    long_format_data_for_upload = this_obs_data.drop(columns=unanimous_concepts)
    long_format_data_for_upload.insert(loc=0, column='resource_id', value=this_resource_id)

    # attach resource_id column to metadata
    metadata_for_upload = this_metadata.copy()
    metadata_for_upload.insert(loc=0, column='resource_id', value=this_resource_id)

    return long_format_data_for_upload, metadata_for_upload


def decode_all_metadata(this_df, metadata_for_upload):
    """
    Take a Dataframe of observations in long format and translate metadata codes into metadata names.
    Use tables in format equal to output of get_upload_data

    """
    this_df_out = this_df.copy()

    for this_col in this_df.columns:

        if this_col in metadata_for_upload['concept_code'].unique():
            ss_metadat = metadata_for_upload.query('concept_code == @this_col')
            new_labels = ss_metadat.set_index('value_code').loc[this_df[this_col].values, 'value_name'].values

            this_df_out.loc[:, this_col] = new_labels

    return this_df_out


def update_data_in_db(this_resource_id, mode='incremental'):

    # upload to SQL
    db_con = get_db_engine('econ_data')

    obs_data_table_name = 'ECB_' + this_resource_id

    if mode == 'incremental':
        # get current maximum date in database
        query=f"""
        SELECT max(TIME_PERIOD)
        FROM {obs_data_table_name}
        """
        curr_max_date = get_db_data(query, db_con).squeeze()
        start_date = (curr_max_date - DateOffset(years=1)).strftime('%Y-%m-%d')
    else:
        start_date = '1900-01-01'

    # get observations
    if this_resource_id == 'CISS':
        all_data = get_ciss_data(start_date)

    elif this_resource_id == 'IRS':
        all_data = get_irs_data(start_date)

    elif this_resource_id == 'YC':
        all_data = get_yc_data(start_date)

    else:
        raise ValueError(f'Data download not implemented yet for resource_id {this_resource_id}')

    # get relevant metadata
    this_decodes_df = get_resource_metadata_decodes(this_resource_id)
    this_metadata = get_metadata_lookup(all_data, this_decodes_df)

    obs_data_for_upload, metadata_for_upload = get_upload_data(this_resource_id, all_data, this_metadata)
    delete_from_date = np.maximum(pd.to_datetime(start_date), obs_data_for_upload['TIME_PERIOD'].min())
    overwrite_db_table_from_df_date_greater_than(obs_data_for_upload, obs_data_table_name, db_con, 'TIME_PERIOD',
                                                 delete_from_date, index=False)

    metadata_table_name = 'ECB_metadata'
    overwrite_db_table_from_df_matching_single_eq_condition(metadata_for_upload, metadata_table_name,
                                                         db_con, 'resource_id', this_resource_id, index=False)

    db_con.dispose()


if __name__=="__main__":

    this_resource_id = 'CISS'
    # this_resource_id = 'IRS'
    # this_resource_id = 'YC'

    update_data_in_db(this_resource_id, 'incremental')
