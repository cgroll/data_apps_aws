import json

from data_apps_aws.src_slash_commands.weather import slash_weather, slackify_forecasts

def lambda_handler(event, context):

    try:
        print(f"Received event:\n{event}\nWith context:\n{context}")
        print(event.keys())

        narrowed_down_text = event['body']
        print(f"Somewhere in here is the slack input text: {narrowed_down_text}")
    except:
        print('Catched error due to unexpected function call')

    forecasts, sun_moon_times = slash_weather()
    table_str = slackify_forecasts(forecasts)
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": table_str,
            "message": 'Not sure whether this is needed',
        }),
    }
