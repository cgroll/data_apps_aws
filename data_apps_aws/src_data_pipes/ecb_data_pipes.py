import pandas as pd
from pandasdmx import Request

from data_apps_aws.sql import overwrite_db_table_from_df, get_db_engine

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
    return this_data.T.reset_index().melt(id_vars=id_vars)


def get_ciss_data():
    """
    Download CISS data. Needs to deal with fact that some time series are monthly and some are daily.
    Since dates are given as TimePeriod, monthly data first needs to be transformed to be concatenated with
    daily timestamps.

    :return: DataFrame with all CISS data in long format
    """
    this_resource_id = 'CISS'

    monthly_data_countries = make_long_format(
        get_ecb_data(this_resource_id, {'FREQ': 'M', 'PROVIDER_FM_ID': 'SOV_CI', 'DATA_TYPE_FM': 'IDX'},
                     {'startPeriod': '2016'}))
    monthly_data_regions = make_long_format(
        get_ecb_data(this_resource_id, {'FREQ': 'M', 'PROVIDER_FM_ID': ['SOV_EW', 'SOV_GDPW']},
                     {'startPeriod': '2016'}))

    monthly_data = pd.concat([monthly_data_countries, monthly_data_regions], axis=0)
    monthly_data['TIME_PERIOD'] = pd.to_datetime([this_tp.to_timestamp(how='E').date() for this_tp in monthly_data['TIME_PERIOD']])

    daily_data_countries = make_long_format(get_ecb_data(this_resource_id, {'FREQ': 'D'}, {'startPeriod': '2016'}))
    daily_data_countries['TIME_PERIOD'] = pd.to_datetime([this_tp.to_timestamp(how='E').date() for this_tp in daily_data_countries['TIME_PERIOD']])

    all_ciss_data = pd.concat([daily_data_countries, monthly_data], axis=0)

    return all_ciss_data


def get_metadata_lookup(this_data_df, this_decodes_df):

    # identify metadata columns
    value_col_names = ['TIME_PERIOD', 'value']
    metadata_cols = [this_col for this_col in this_data_df.columns.values if this_col not in value_col_names]

    # get list of all occurring values
    this_data_occur_metadata = this_data_df.loc[:, metadata_cols]
    this_data_occur_metadata = this_data_occur_metadata .melt().drop_duplicates()
    this_data_occur_metadata .columns = ['concept_code', 'value_code']

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

def get_ciss_upload_data():

    this_resource_id = 'CISS'

    # get observations
    if this_resource_id == 'CISS':
        all_data = get_ciss_data()
    else:
        raise ValueError(f'Data download not implemented yet for resource_id {this_resource_id}')

    # get relevant metadata
    this_decodes_df = get_resource_metadata_decodes(this_resource_id)
    this_metadata = get_metadata_lookup(all_data, this_decodes_df)

    obs_data_for_upload, metadata_for_upload = get_upload_data(this_resource_id, all_data, this_metadata)

    # upload to SQL
    db_con = get_db_engine('econ_data')

    obs_data_table_name = 'ECB_' + this_resource_id
    overwrite_db_table_from_df(obs_data_for_upload, obs_data_table_name, db_con, index=False)

    metadata_table_name = 'ECB_metadata'
    overwrite_db_table_from_df(metadata_for_upload, metadata_table_name, db_con, index=False)

    return obs_data_for_upload, metadata_for_upload


if __name__=="__main__":

    obs_data_for_upload, metadata_for_upload = get_ciss_upload_data()

    obs_data_for_upload.head(4)