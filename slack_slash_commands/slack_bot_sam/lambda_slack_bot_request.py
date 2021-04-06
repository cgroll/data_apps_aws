import json

payload = {'blocks': [{'type': 'section', 'text': {'type': 'mrkdwn', 'text': "Hello, Assistant to the Regional Manager Dwight! *Michael Scott* wants to know where you'd like to take the Paper Company investors to dinner tonight.\n\n *Please select a restaurant:*"}}, {'type': 'divider'}, {'type': 'section', 'text': {'type': 'mrkdwn', 'text': '*Farmhouse Thai Cuisine*\n:star::star::star::star: 1528 reviews\n They do have some vegan options, like the roti and curry, plus they have a ton of salad stuff and noodles can be ordered without meat!! They have something for everyone here'}, 'accessory': {'type': 'image', 'image_url': 'https://s3-media3.fl.yelpcdn.com/bphoto/c7ed05m9lC2EmA3Aruue7A/o.jpg', 'alt_text': 'alt text for image'}}, {'type': 'section', 'text': {'type': 'mrkdwn', 'text': '*Kin Khao*\n:star::star::star::star: 1638 reviews\n The sticky rice also goes wonderfully with the caramelized pork belly, which is absolutely melt-in-your-mouth and so soft.'}, 'accessory': {'type': 'image', 'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/korel-1YjNtFtJlMTaC26A/o.jpg', 'alt_text': 'alt text for image'}}, {'type': 'section', 'text': {'type': 'mrkdwn', 'text': '*Ler Ros*\n:star::star::star::star: 2082 reviews\n I would really recommend the  Yum Koh Moo Yang - Spicy lime dressing and roasted quick marinated pork shoulder, basil leaves, chili & rice powder.'}, 'accessory': {'type': 'image', 'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/DawwNigKJ2ckPeDeDM7jAg/o.jpg', 'alt_text': 'alt text for image'}}, {'type': 'divider'}, {'type': 'actions', 'elements': [{'type': 'button', 'text': {'type': 'plain_text', 'text': 'Farmhouse', 'emoji': True}, 'value': 'click_me_123'}, {'type': 'button', 'text': {'type': 'plain_text', 'text': 'Kin Khao', 'emoji': True}, 'value': 'click_me_123', 'url': 'https://google.com'}, {'type': 'button', 'text': {'type': 'plain_text', 'text': 'Ler Ros', 'emoji': True}, 'value': 'click_me_123', 'url': 'https://google.com'}]}]}

table_str = '+-------------+-------+\n| dawn        | 06:11 |\n+-------------+-------+\n| sunrise     | 06:43 |\n+-------------+-------+\n| suntransit  | 13:16 |\n+-------------+-------+\n| sunset      | 19:49 |\n+-------------+-------+\n| dusk        | 20:21 |\n+-------------+-------+\n| moonrise    | 04:07 |\n+-------------+-------+\n| moontransit | 08:13 |\n+-------------+-------+\n| moonset     | 12:22 |\n+-------------+-------+'

table_str = 'date          min_temp    max_temp    sun_hours    rain_prob    rain_sum  forecast             weather\n----------  ----------  ----------  -----------  -----------  ----------  -------------------  ----------------------\n2021-04-05           0          14            5           90        4.94  :cloud:              bedeckt\n2021-04-06          -3           2            3           90        2.98  :snow_cloud:         leichter Schneeschauer\n2021-04-07          -2           3            1           90        5.21  :snow_cloud:         leichter Schneeschauer\n2021-04-08          -1           7            8           25        0     :sunny:              sonnig\n2021-04-09          -3          16            3            0        0     :cloud:              bedeckt\n2021-04-10           5          16            6           20        0     :barely_sunny:       wolkig\n2021-04-11           3          10            5            0        0     :partly_sunny:       leicht bewölkt\n2021-04-12           3          13            7            0        0     :partly_sunny:       leicht bewölkt\n2021-04-13           5          13            9            0        0     :partly_sunny:       leicht bewölkt\n2021-04-14           6          14            7            0        0     :partly_sunny:       leicht bewölkt\n2021-04-15           1           2            0           15        0.38  :cloud:              bedeckt\n2021-04-16           1           3            0           15        0.69  :partly_sunny_rain:  leichter Regen\n2021-04-17           0           5            0           15        1.12  :partly_sunny_rain:  leichter Regen\n2021-04-18          -1           2            0           15        1.67  :question:           leichter Schneefall'


def lambda_handler(event, context):
    print(f"Received event:\n{event}\nWith context:\n{context}")
    print(event.keys())

    narrowed_down_text = event['body']
    print(f"Somewhere in here is the slack input text: {narrowed_down_text}")

    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": table_str,
            "message": 'Not sure whether this is needed',
        }),
    }
    
    # return {
        # "statusCode": 200,
        # "body": json.dumps({
            # "text": 'Here is a link: <https://youtu.be/frszEJb0aOo|General Kenobi!>. :smile: This is a text with `inline *code*` in it.\n- water\n- bread\n - salt,',
            # "message": 'HELLO WORLD',
        # }),
    # }
