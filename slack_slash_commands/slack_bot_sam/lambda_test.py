import json
from urllib import parse as urlparse

payload = {'blocks': [{'type': 'section', 'text': {'type': 'mrkdwn', 'text': "Hello, Assistant to the Regional Manager Dwight! *Michael Scott* wants to know where you'd like to take the Paper Company investors to dinner tonight.\n\n *Please select a restaurant:*"}}, {'type': 'divider'}, {'type': 'section', 'text': {'type': 'mrkdwn', 'text': '*Farmhouse Thai Cuisine*\n:star::star::star::star: 1528 reviews\n They do have some vegan options, like the roti and curry, plus they have a ton of salad stuff and noodles can be ordered without meat!! They have something for everyone here'}, 'accessory': {'type': 'image', 'image_url': 'https://s3-media3.fl.yelpcdn.com/bphoto/c7ed05m9lC2EmA3Aruue7A/o.jpg', 'alt_text': 'alt text for image'}}, {'type': 'section', 'text': {'type': 'mrkdwn', 'text': '*Kin Khao*\n:star::star::star::star: 1638 reviews\n The sticky rice also goes wonderfully with the caramelized pork belly, which is absolutely melt-in-your-mouth and so soft.'}, 'accessory': {'type': 'image', 'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/korel-1YjNtFtJlMTaC26A/o.jpg', 'alt_text': 'alt text for image'}}, {'type': 'section', 'text': {'type': 'mrkdwn', 'text': '*Ler Ros*\n:star::star::star::star: 2082 reviews\n I would really recommend the Yum Koh Moo Yang - Spicy lime dressing and roasted quick marinated pork shoulder, basil leaves, chili & rice powder.'}, 'accessory': {'type': 'image', 'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/DawwNigKJ2ckPeDeDM7jAg/o.jpg', 'alt_text': 'alt text for image'}}, {'type': 'divider'}, {'type': 'actions', 'elements': [{'type': 'button', 'text': {'type': 'plain_text', 'text': 'Farmhouse', 'emoji': True}, 'value': 'click_me_123'}, {'type': 'button', 'text': {'type': 'plain_text', 'text': 'Kin Khao', 'emoji': True}, 'value': 'click_me_123', 'url': 'https://google.com'}, {'type': 'button', 'text': {'type': 'plain_text', 'text': 'Ler Ros', 'emoji': True}, 'value': 'click_me_123', 'url': 'https://google.com'}]}]}

def lambda_handler(event, context):

    try:
        print(f"Received event:\n{event}\nWith context:\n{context}")
        print(event.keys())

        # msg_map = dict(urlparse.parse_qsl(base64.b64decode(str(event['body'])).decode('ascii')))
        msg_map = dict(urlparse.parse_qsl(event['body']))
        command = msg_map.get('command','err')  # will be /command name

        print(f'Command: {command}')
        
        user_input = msg_map.get('text','err')
        print(f'Params: {user_input}')

        output = user_input
        payload = {'blocks': [
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_section",
                        "elements": [
                            {
                                "type": "text",
                                "text": output,
                                "style": {
                                    "code": True
                                }
                            }
                        ]
                    }
                ]
            }
        ]}

        narrowed_down_text = event['body']
        print(f"Somewhere in here is the slack input text: {narrowed_down_text}")
    except:
        print('Catched error due to unexpected function call')
        output = 'There was a problem in the python code'
    
    return {
        "statusCode": 200,
        "body": json.dumps(payload),
    }
