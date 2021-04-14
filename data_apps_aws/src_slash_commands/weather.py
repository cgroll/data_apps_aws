import requests
import json
import pandas as pd
from tabulate import tabulate

from data_apps_aws.password_manager import get_api_token

def get_location_url():
    # coordinates home
    lat = 48.11721
    long = 11.64806

    url = f"https://forecast-history2.p.rapidapi.com/rapidapi/forecast/{lat}/{long}/summary/"

    return url

def query_api():

    url = get_location_url()

    # set up connection to FRED with API key
    rapid_api_key = get_api_token('rapidAPI')

    headers = {
        'x-rapidapi-key': rapid_api_key,
        'x-rapidapi-host': "forecast-history2.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers)

    return response

def get_astronomy_info(response_dict):

    this_date_forecast = response_dict['items'][0]
    astronomy_dict = this_date_forecast['astronomy'].copy()

    del astronomy_dict['moonphase']
    del astronomy_dict['moonzodiac']

    sun_moon_times = pd.DataFrame.from_dict(astronomy_dict, orient='index', columns=['datetime'])
    sun_moon_times['datetime'] = pd.to_datetime(sun_moon_times['datetime'])
    sun_moon_times['time'] = [this_datetime.strftime('%H:%M') for this_datetime in sun_moon_times['datetime']]

    return sun_moon_times

def get_weather_info(response_dict):

    all_dates = [this_date_data['date'] for this_date_data in response_dict['items']]
    all_weekdays = [pd.to_datetime(this_date).strftime('%a') for this_date in all_dates]
    forecasts = pd.DataFrame(all_weekdays, index=all_dates, columns=['day'])

    forecasts['min_temp'] = [this_date_data['temperature']['min'] for this_date_data in response_dict['items']]
    forecasts['max_temp'] = [this_date_data['temperature']['max'] for this_date_data in response_dict['items']]
    forecasts['sun_hours'] = [this_date_data['sunHours'] for this_date_data in response_dict['items']]
    forecasts['rain_prob'] = [this_date_data['prec']['probability'] for this_date_data in response_dict['items']]
    forecasts['rain_sum'] = [this_date_data['prec']['sum'] for this_date_data in response_dict['items']]
    forecasts['snow'] = [this_date_data['freshSnow'] for this_date_data in response_dict['items']]
    forecasts['weather'] = [this_date_data['weather']['text'] for this_date_data in response_dict['items']]

    forecasts = forecasts.drop(columns=['snow'])

    forecasts.index.name = 'date'

    return forecasts

def process_response(response):

    response_dict = json.loads(response.text)

    forecast_date = pd.to_datetime(response_dict['forecastDate'])
    next_update = pd.to_datetime(response_dict['nextUpdate'])
    print(f'Current forecast date: {forecast_date}, tz: {forecast_date.tz}')
    print(f'Next update: {next_update}, tz: {next_update.tz}')

    forecasts = get_weather_info(response_dict)
    sun_moon_times = get_astronomy_info(response_dict)


    return forecasts, sun_moon_times

def slash_weather():

    response = query_api()
    forecasts, sun_moon_times = process_response(response)

    return forecasts, sun_moon_times


def emojify_weather(forecasts_export):

    emoji_map = {'bedeckt': ':cloud:',
                 'leichter Schneeschauer': ':snow_cloud:',
                 'sonnig': ':sunny:',
                 'wolkig': ':barely_sunny:',
                 'leicht bewölkt': ':partly_sunny:',
                 'leichter Regen': ':partly_sunny_rain:',
                 'leichter Schneefall': ':snow_cloud:',
                 }

    weather_emojis = forecasts_export['weather'].map(emoji_map)
    weather_emojis = weather_emojis.fillna(':question:')
    forecasts_export.insert(forecasts_export.shape[1] - 1, 'forecast', weather_emojis)

    return forecasts_export

def slackify_forecasts(forecasts):

    forecasts_export = forecasts.reset_index()
    forecasts_export = emojify_weather(forecasts_export)

    # translate to table print string
    table_str = tabulate(forecasts_export, tablefmt="simple", headers="keys", showindex=False)

    table_str_payload = {'blocks': [
        {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {
                            "type": "text",
                            "text": table_str,
                            "style": {
                                "code": True
                            }
                        }
                    ]
                }
            ]
        }
    ]}

    return table_str_payload

def slackify_sun_moon_times(sun_moon_times):

    table_str = tabulate(sun_moon_times[['time']], tablefmt="grid")

    return table_str

if __name__=="__main__":

    forecasts, sun_moon_times = slash_weather()
    table_str = slackify_forecasts(forecasts)
    print(table_str)
