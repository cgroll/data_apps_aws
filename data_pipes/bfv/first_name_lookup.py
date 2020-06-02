from bs4 import BeautifulSoup
import requests
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import numpy as np
import re
import os
import time
from datetime import datetime
from data_apps_aws.sql import *
from requests import get


def extract_name_info_from_webpage(this_first_name):

    this_first_name_url = "https://www.vorname.com/name," + this_first_name + ".html"

    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get(this_first_name_url)
    driver.implicitly_wait(10)

    try:
        error_elem = driver.find_element_by_class_name('error404')
        if driver.find_element_by_class_name('error404') is not None:
            return None

    except:

        for ii in np.arange(0, 40):
            driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)

        time.sleep(1)

        # click read more button
        python_button = driver.find_element_by_class_name('read-more-container')
        python_button.click()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        driver.quit()

        all_section_container_list = soup.find_all('div', {'class': 'separator_line'})

        name_lookup_results = {'first_name': this_first_name}

        for this_section in all_section_container_list:

            section_title_component = this_section.find('h2', {'class': 'section__title'})

            if section_title_component is not None:

                # print(section_title_component.get("data-addfunc"))

                if section_title_component.get("data-addfunc") == 'herkunft':

                    this_content = this_section.contents[2]
                    if this_content == '\n':
                        this_content = this_section.contents[3]

                    if this_content.name == 'p':
                        this_content = this_content.text
                    else:
                        this_content = this_content.replace('\n', '').lstrip().rstrip()

                    name_lookup_results['Herkunft'] = this_content

                elif section_title_component.get("data-addfunc") == 'sprachen':

                    this_content = this_section.contents[2]
                    if this_content == '\n':
                        this_content = this_section.contents[3]

                    if this_content.name == 'p':
                        this_content = this_content.text.replace('\n', '').lstrip().rstrip()
                    else:
                        this_content = this_content.replace('\n', '').lstrip().rstrip()

                    name_lookup_results['Sprachen'] = this_content


        name_results_df = pd.DataFrame.from_dict({0: name_lookup_results}, orient='index')

        return name_results_df


def page_scan_logging(this_first_name, success, skipped):

    job_metadata_entry = {0: {'first_name': this_first_name,
                              'success': success,
                              'skipped': skipped,
                              'time_of_scan': datetime.now()
                              }}
    job_metadata_row = pd.DataFrame.from_dict(job_metadata_entry, orient='index')

    # upload to SQL
    db_con = get_db_engine('bfv_data')

    overwrite_db_table_from_df_matching_single_eq_condition(job_metadata_row,
                                                            'page_scan_logging_first_name', db_con,
                                                            'first_name', this_first_name)

    db_con.dispose()

    #job_metadata_row.to_sql('page_scan_logging_first_name', db_con.engine, index=False)


if __name__=="__main__":

    db_con = get_db_engine('bfv_data')

    query = """
    SELECT first_name
    FROM match_participants
    """

    all_first_names = get_db_data(query, db_con)['first_name'].unique()

    query = """
    SELECT *
    FROM page_scan_logging_first_name
    """

    all_past_scans = get_db_data(query, db_con)
    all_scanned_names = all_past_scans['first_name'].values
    all_failed_scanned_names = all_past_scans.query('success == 0 & skipped == 0')['first_name'].values

    for this_first_name in all_first_names:

        if this_first_name not in all_failed_scanned_names:
            continue

        try:
            name_results_df = extract_name_info_from_webpage(this_first_name)

            if name_results_df is None:
                page_scan_logging(this_first_name, success=False, skipped=True)
                print(f'{this_first_name}: skipped')

            else:
                db_con = get_db_engine('bfv_data')

                # for first-time creation of tables:
                #name_results_df.to_sql('first_name_lookup', db_con.engine, index=False)

                # update in database
                overwrite_db_table_from_df_matching_single_eq_condition(name_results_df,
                                                                        'first_name_lookup', db_con,
                                                                        'first_name', this_first_name)

                db_con.dispose()

                page_scan_logging(this_first_name, success=True, skipped=False)
                print(f'{this_first_name}: success')

        except:

            page_scan_logging(this_first_name, success=False, skipped=False)
            print(f'{this_first_name}: failed')





