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


def get_championship_url(this_championship_id):

    return 'https://www.bfv.de/wettbewerbe/meisterschaften/' + this_championship_id + '#tabelle'


def open_url_cookie_accept(this_url):

    # chrome session
    driver = webdriver.Chrome(executable_path='./chromedriver')
    driver.get(this_url)
    driver.implicitly_wait(10)

    #time.sleep(1)

    # accept cookies
    python_button = driver.find_element_by_id('uc-btn-accept-banner')
    python_button.click()

    return driver


def extract_final_table(driver):

    ## get final championship table
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    all_teams_container_list = soup.find_all('tr', {'class': 'bfv-table-entry bfv-table-entry--data'})

    all_team_results = None

    for this_team_container in all_teams_container_list:

        # extract team name and url
        this_team_link = this_team_container.find('a').get('href')
        this_team_name = this_team_container.find('a').get_text().replace('\n', '').rstrip().lstrip()

        # extract values from table
        comp_names = []
        comp_values = []

        for this_component in this_team_container.find_all('td'):
            this_component_name = this_component.get('class')[1].split('--')[1]
            this_component_value = this_component.get_text().replace('\n', '').rstrip().lstrip()

            comp_names.append(this_component_name)
            comp_values.append(this_component_value)

        comp_names.append('link')
        comp_values.append(this_team_link)

        this_team_table_values = pd.Series(comp_values, index=comp_names, name=this_team_name)

        if all_team_results is None:
            all_team_results = this_team_table_values
        else:
            all_team_results = pd.concat([all_team_results, this_team_table_values], axis=1)

    return all_team_results.T


def proceed_to_fairness_table(driver):

    time.sleep(2)
    driver.find_element_by_tag_name('body').send_keys(Keys.UP)

    # find fairness navigation link
    all_navigation_links = driver.find_elements_by_class_name('tab-navigation__link')

    for this_navigation_link in all_navigation_links:

        if this_navigation_link.get_attribute('title') == 'Fairness':

            driver.find_element_by_tag_name('body').send_keys(Keys.UP)
            # time.sleep(4)
            driver.find_element_by_tag_name('body').send_keys(Keys.UP)

            time.sleep(2)

            this_navigation_link.click()
            time.sleep(2)

            return


def extract_fairness_table(driver):

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    all_teams_container_list = soup.find_all('td', {'class': 'bfv-table-collapsed-entry__inner-table'})

    list_of_metrics = ['matches', 'yellowcards', 'yellowredcards', 'redcards', 'timepenalties',
                       'unsportsmanlike', 'gamefailures', 'gamecrashes', 'fscore', 'quote']

    all_team_metrics = None

    for this_team_container in all_teams_container_list:

        # extract team name
        this_team_name_raw = this_team_container.find('div',
                                                      {'class': 'bfv-table-collapsed-entry__team-name'}).get_text()
        this_team_name = this_team_name_raw.replace('\n', '').rstrip().lstrip()

        # extract team metrics
        this_team_metrics_list = this_team_container.find_all('div', {'class': 'bfv-table-collapsed-entry__data-value'})
        metrics = [float(this_metrics.get_text().replace('\n', '').rstrip().lstrip()) for this_metrics in
                   this_team_metrics_list]

        this_team_row = pd.Series(metrics, name=this_team_name, index=list_of_metrics)

        if all_team_metrics is None:
            all_team_metrics = this_team_row
        else:
            all_team_metrics = pd.concat([all_team_metrics, this_team_row], axis=1)

    return all_team_metrics.T


def page_scan_logging(this_league_id, job_type, success, skipped):

    # job types
    # - league_tables: league_id, table_type
    # - matchday_games: league_id, matchday
    # - games_players: league_id, match

    job_metadata_entry = {0: {'league_id': this_league_id,
                              'job_type': job_type,
                              'success': success,
                              'skipped': skipped,
                              'time_of_scan': datetime.now()
                              }}
    job_metadata_row = pd.DataFrame.from_dict(job_metadata_entry, orient='index')

    # upload to SQL
    db_con = get_db_engine('bfv_data')

    overwrite_db_table_from_df_matching_multiple_eq_condition(job_metadata_row,
                                                            'page_scan_logging', db_con,
                                                            league_id=this_league_id,
                                                            job_type=job_type
                                                            )

    db_con.dispose()

    #job_metadata_row.to_sql('page_scan_logging', db_con.engine, index=False)
    #job_metadata_row.to_sql('PROD_run_id_scans', sql_con.engine, index=False)


def single_league_tables_task(this_championship_id):

    this_championship_overview_url = get_championship_url(this_championship_id)

    # open webpage and accept cookies
    driver = open_url_cookie_accept(this_championship_overview_url)

    # get final table
    final_table = extract_final_table(driver)
    final_table.insert(0, 'championship_id', this_championship_id)

    # move on to fairness table
    proceed_to_fairness_table(driver)

    fairness_table = extract_fairness_table(driver)
    fairness_table = fairness_table.reset_index()
    fairness_table.rename({'index': 'team'}, axis=1, inplace=True)
    fairness_table.insert(0, 'championship_id', this_championship_id)

    driver.quit()

    db_con = get_db_engine('bfv_data')

    # for first-time creation of tables:
    # final_table.to_sql('final_tables', db_con.engine, index=False)
    # fairness_table.to_sql('fairness_tables', db_con.engine, index=False)

    # update in database
    overwrite_db_table_from_df_matching_single_eq_condition(final_table, 'final_tables',
                                                            db_con, 'championship_id', this_championship_id,
                                                            index=False)
    overwrite_db_table_from_df_matching_single_eq_condition(fairness_table, 'fairness_tables',
                                                            db_con, 'championship_id', this_championship_id,
                                                            index=False)

    db_con.dispose()

    # do some logging
    page_scan_logging(this_championship_id, "league_tables", success=True, skipped=False)


def scrape_match_day_match_links(driver):

    # extract content
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # all_match_info_list = soup.body.find_all('div', {'class': 'bfv-matchdata-result__body'})
    # this_match_info = all_match_info_list[0]

    all_game_link_components = soup.body.find_all('a', {'class': 'bfv-spieltag-eintrag__match-link'})

    all_game_links = [this_game_link.get('href') for this_game_link in all_game_link_components]

    match_day_match_links = pd.DataFrame(all_game_links, columns=['link'])

    return match_day_match_links


def single_match_day_task(this_championship_id, this_match_day):

    this_match_day_url = 'https://www.bfv.de/wettbewerbe/meisterschaften/' + this_championship_id + '#spieltag=' + str(
        this_match_day)

    # open webpage and accept cookies
    driver = open_url_cookie_accept(this_match_day_url)

    time.sleep(2)

    for ii in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
        driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)

    # extract links
    match_day_match_links = scrape_match_day_match_links(driver)
    driver.quit()

    # attach metadata
    match_day_match_links.insert(0, 'match_day', this_match_day)
    match_day_match_links.insert(0, 'championship_id', this_championship_id)

    db_con = get_db_engine('bfv_data')

    # for first-time creation of tables:
    #match_day_match_links.to_sql('match_day_links', db_con.engine, index=False)

    # update in database
    overwrite_db_table_from_df_matching_multiple_eq_condition(match_day_match_links, 'match_day_links',
                                                              db_con, championship_id=this_championship_id,
                                                              match_day=this_match_day)

    db_con.dispose()

    # do some logging
    link_prefix = 'https://www.bfv.de/wettbewerbe/meisterschaften/'
    match_day_id = this_match_day_url.split(link_prefix)[1]
    page_scan_logging(match_day_id, "matchday_games", success=True, skipped=False)


def get_id_from_url(this_url, this_prefix):
    return this_url.split(this_prefix)[1]


def navigate_to_aufstellung(driver):

    # scroll down
    for ii in np.arange(0, 20):
        driver.find_element_by_tag_name('body').send_keys(Keys.DOWN)

    time.sleep(2)

    # find from class tab-navigation__link the one with title "Aufstellung" and click it
    all_tabs = driver.find_elements_by_class_name('tab-navigation__link')

    for this_tab in all_tabs:
        if this_tab.get_attribute('title') == "Aufstellung":
            this_tab.click()

    return driver


def extract_match_participants(driver, this_match_id):

    # extract values from page
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    teams_span_list = soup.find_all("span", {'class': 'bfv-tab-switch__tab-text'})
    team_names = [this_team_span.get_text() for this_team_span in teams_span_list]

    team_contents = soup.find_all('div', {'class': 'bfv-composition__team js-bfv-tab-switch__content'})
    all_people = None

    for this_iter in [0, 1, 2, 3, 4, 5]:

        all_player_names = []
        all_player_urls = []

        if this_iter in [0, 1]:
            this_type = "starting"
        elif this_iter in [2, 3]:
            this_type = 'bench'
        elif this_iter in [4, 5]:
            this_type = 'trainer'

        this_team_contents = team_contents[this_iter]

        for this_team_entry in this_team_contents.find_all('a'):

            team_info_raw = this_team_entry.find_all('span', {'class': 'bfv-composition-entry__team-name'})

            if len(team_info_raw) > 0:
                if this_iter == 0:
                    home_team_name = team_info_raw[0].get_text()
                    home_team_id = team_info_raw[0].get('id')
                elif this_iter == 1:
                    away_team_name = team_info_raw[0].get_text()
                    away_team_id = team_info_raw[0].get('id')

            else:
                this_player_name = this_team_entry.get_text().replace('\n', '').rstrip().lstrip()
                this_player_url = this_team_entry.get('href')

                all_player_names.append(this_player_name)
                all_player_urls.append(this_player_url)

        these_people = pd.concat(
            [pd.Series(all_player_names, name='player_name'), pd.Series(all_player_urls, name='player_url')],
            axis=1)
        these_people['type'] = this_type

        if this_iter in [0, 2, 4]:
            these_people['team'] = home_team_name
            these_people['team_id'] = home_team_id

        elif this_iter in [1, 3, 5]:
            these_people['team'] = away_team_name
            these_people['team_id'] = away_team_id

        if all_people is None:
            all_people = these_people
        else:
            all_people = pd.concat([all_people, these_people], axis=0)

    all_people.reset_index(inplace=True, drop=True)

    # get all player IDs
    all_player_ids = []
    for this_player_url in all_people['player_url']:

        if this_player_url is None:
            all_player_ids.append(None)
        else:
            link_prefix = 'https://www.bfv.de/spieler/'
            this_player_id = this_player_url.split(link_prefix)[1]
            all_player_ids.append(this_player_id)

    all_people['person_id'] = all_player_ids

    all_people.insert(0, 'match_id', this_match_id)

    all_first_names = []
    for this_name in all_people['player_name']:
        all_first_names.append(this_name.split(' ')[0].replace(',', '').strip())

    all_people['first_name'] = all_first_names

    return all_people


def single_match_participants_task(this_match_url):

    this_match_id = get_id_from_url(this_match_url, 'https://www.bfv.de/spiele/')
    driver = open_url_cookie_accept(this_match_url)
    time.sleep(2)
    driver = navigate_to_aufstellung(driver)
    time.sleep(2)
    all_participants = extract_match_participants(driver, this_match_id)
    driver.quit()

    db_con = get_db_engine('bfv_data')

    # for first-time creation of tables:
    #all_participants.to_sql('match_participants', db_con.engine, index=False)

    # update in database
    this_match_id = get_id_from_url(this_match_url, 'https://www.bfv.de/spiele/')
    overwrite_db_table_from_df_matching_multiple_eq_condition(all_participants, 'match_participants',
                                                              db_con, match_id=this_match_id)

    db_con.dispose()

    # do some logging
    page_scan_logging(this_match_id, "match_participants", success=True, skipped=False)


if __name__=="__main__":

    # settings
    job_type = 'match_participants' # league_tables, matchday_games, match_participants
    job_type = 'league_tables'
    match_days = [9, 19]


    if job_type == 'league_tables':

        all_leagues_with_links = pd.read_csv('./bfv_league_links.csv')

        for this_link in all_leagues_with_links['Link']:

            this_championship_id = get_id_from_url(this_link, 'https://www.bfv.de/wettbewerbe/meisterschaften/')

            print(f'Scraping championship {this_championship_id}')

            try:
                # extract data and upload
                single_league_tables_task(this_championship_id)

            except:
                page_scan_logging(this_championship_id, "league_tables", success=False, skipped=False)

    elif job_type == 'matchday_games':

        all_leagues_with_links = pd.read_csv('./bfv_league_links.csv')

        for this_link in all_leagues_with_links['Link']:

            this_championship_id = get_id_from_url(this_link, 'https://www.bfv.de/wettbewerbe/meisterschaften/')

            for this_match_day in match_days:

                print(f'Scraping match day games for {this_championship_id} and match day {this_match_day}')

                try:
                    single_match_day_task(this_championship_id, this_match_day)

                except:

                    this_match_day_url = 'https://www.bfv.de/wettbewerbe/meisterschaften/' + this_championship_id + '#spieltag=' + str(
                        this_match_day)

                    match_day_id = get_id_from_url(this_match_day_url, 'https://www.bfv.de/wettbewerbe/meisterschaften/')

                    page_scan_logging(match_day_id, "matchday_games", success=False, skipped=False)


    elif job_type == 'match_participants':

        db_con = get_db_engine('bfv_data')
        query="""
        SELECT link
        FROM match_day_links
        """
        all_match_urls = get_db_data(query, db_con).values.flatten()

        query="""
        SELECT league_id
        FROM page_scan_logging
        WHERE job_type = "match_participants"
        AND success = 0
        """
        all_failed_match_ids = get_db_data(query, db_con).values.flatten()

        query="""
        SELECT league_id
        FROM page_scan_logging
        WHERE job_type = "match_participants"
        """
        all_scanned_match_ids = get_db_data(query, db_con).values.flatten()

        for this_match_url in all_match_urls:

            if this_match_url is None:
                continue

            this_match_id = get_id_from_url(this_match_url, 'https://www.bfv.de/spiele/')
            if this_match_id not in all_failed_match_ids:
                continue

            #if this_match_id in all_scanned_match_ids:
            #    continue

            print(f'Scraping participants for match {this_match_url}')

            try:
                single_match_participants_task(this_match_url)

            except:

                this_match_id = get_id_from_url(this_match_url, 'https://www.bfv.de/spiele/')
                page_scan_logging(this_match_id, "match_participants", success=False, skipped=False)











