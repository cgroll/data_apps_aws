from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import pandas as pd

from data_apps_aws.sql import *

def page_scan_logging(this_name, name_type, success, skipped):
    # name
    # name_type
    # success
    # skipped
    # time_of_scan

    job_metadata_entry = {0: {'name': this_name,
                              'name_type': name_type,
                              'success': success,
                              'skipped': skipped
                              }}
    job_metadata_row = pd.DataFrame.from_dict(job_metadata_entry, orient='index')

    # upload to SQL
    db_con = get_db_engine('bfv_data')

    # initialize table
    # job_metadata_row.to_sql('page_scan_logging_forebears', db_con.engine, index=False)

    overwrite_db_table_from_df_matching_multiple_eq_condition(job_metadata_row,
                                                              'page_scan_logging_forebears', db_con,
                                                              name=this_name,
                                                              name_type=name_type
                                                              )

    db_con.dispose()


def extract_forename_info_from_page(this_name_in):
    """
    Extract name statistics from forebears webpage
    """

    this_name = this_name_in.lower()
    this_name_type = 'forename'

    # get url
    this_url = 'https://forebears.io/forenames/' + this_name

    # get homepage content
    req = Request(this_url, headers={'User-Agent': 'Mozilla/5.0'})
    content = urlopen(req).read()
    soup = BeautifulSoup(content, 'html.parser')

    # search name statistics table
    all_page_tables = soup.find_all('table', {'class': 'table nation-table forename-table'})

    if len(all_page_tables) == 0:
        raise ValueError('No table found')

    table_rows = all_page_tables[0].find('tbody').find_all('tr')

    all_countries = []
    all_counts = []

    for this_row in table_rows:
        all_countries.append(this_row.find_all('td')[0].text)

        # name incidents as number
        this_n_incidence_str = this_row.find_all('td')[2].text
        this_n_incidence = int(this_n_incidence_str.replace(',', ''))
        all_counts.append(this_n_incidence)

    name_counts = pd.DataFrame(all_counts, index=all_countries)
    name_counts = name_counts.reset_index()
    name_counts.columns = ['country', 'name_count']
    name_counts.insert(0, 'name', this_name)
    name_counts.insert(0, 'name_type', this_name_type)

    return name_counts




if __name__=="__main__":

    this_name_type = 'forename'
    sql_result_table_name = 'forebears_name_lookup'

    if this_name_type == 'forename':
        db_con = get_db_engine('bfv_data')

        query = """
        SELECT first_name
        FROM match_participants
        """

        all_first_names = get_db_data(query, db_con)['first_name'].unique()
        all_names = all_first_names
    else:
        all_names = []

    query = """
    SELECT *
    FROM page_scan_logging_forebears
    """

    all_past_scans = get_db_data(query, db_con)
    all_past_scans = all_past_scans.query('name_type == @this_name_type')

    all_success_scans = all_past_scans.query('success == 1')['name'].values
    #all_scanned_names = all_past_scans['name'].values
    #all_failed_scanned_names = all_past_scans.query('success == 0 & skipped == 0')['first_name'].values

    for this_name in all_names:

        this_name_escaped = this_name

        this_name_escaped = this_name_escaped.replace('ü', '%C3%BC')
        this_name_escaped = this_name_escaped.replace('Ü', '%C3%BC')
        this_name_escaped = this_name_escaped.replace('ö', '%C3%B6')
        this_name_escaped = this_name_escaped.replace('Ö', '%C3%B6')
        this_name_escaped = this_name_escaped.replace('ä', '%C3%A4')
        this_name_escaped = this_name_escaped.replace('Ä', '%C3%A4')

        # skip already successful scans
        if this_name in all_success_scans:
            print(f'{this_name}: skipped, already successful before')
            continue

        try:
            name_counts_df = extract_forename_info_from_page(this_name_escaped)
            name_counts_df['name'] = this_name

            if name_counts_df is None:
                page_scan_logging(this_name, this_name_type, success=False, skipped=True)
                print(f'{this_name}: skipped')

            else:
                db_con = get_db_engine('bfv_data')

                # for first-time creation of tables:
                # name_counts_df.to_sql(sql_result_table_name, db_con.engine, index=False)

                # update in database
                overwrite_db_table_from_df_matching_multiple_eq_condition(name_counts_df,
                                                                          sql_result_table_name,
                                                                          db_con,
                                                                          name=this_name,
                                                                          name_type=this_name_type
                                                                          )

                db_con.dispose()

                page_scan_logging(this_name, this_name_type, success=True, skipped=False)
                print(f'{this_name}: success')

        except:

            page_scan_logging(this_name, this_name_type, success=False, skipped=False)
            print(f'{this_name}: failed')

