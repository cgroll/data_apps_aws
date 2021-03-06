import logging
import json
from flask import Flask, jsonify

payload = {'blocks': [{'type': 'section', 'text': {'type': 'mrkdwn', 'text': "Hello, Assistant to the Regional Manager Dwight! *Michael Scott* wants to know where you'd like to take the Paper Company investors to dinner tonight.\n\n *Please select a restaurant:*"}}, {'type': 'divider'}, {'type': 'section', 'text': {'type': 'mrkdwn', 'text': '*Farmhouse Thai Cuisine*\n:star::star::star::star: 1528 reviews\n They do have some vegan options, like the roti and curry, plus they have a ton of salad stuff and noodles can be ordered without meat!! They have something for everyone here'}, 'accessory': {'type': 'image', 'image_url': 'https://s3-media3.fl.yelpcdn.com/bphoto/c7ed05m9lC2EmA3Aruue7A/o.jpg', 'alt_text': 'alt text for image'}}, {'type': 'section', 'text': {'type': 'mrkdwn', 'text': '*Kin Khao*\n:star::star::star::star: 1638 reviews\n The sticky rice also goes wonderfully with the caramelized pork belly, which is absolutely melt-in-your-mouth and so soft.'}, 'accessory': {'type': 'image', 'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/korel-1YjNtFtJlMTaC26A/o.jpg', 'alt_text': 'alt text for image'}}, {'type': 'section', 'text': {'type': 'mrkdwn', 'text': '*Ler Ros*\n:star::star::star::star: 2082 reviews\n I would really recommend the  Yum Koh Moo Yang - Spicy lime dressing and roasted quick marinated pork shoulder, basil leaves, chili & rice powder.'}, 'accessory': {'type': 'image', 'image_url': 'https://s3-media2.fl.yelpcdn.com/bphoto/DawwNigKJ2ckPeDeDM7jAg/o.jpg', 'alt_text': 'alt text for image'}}, {'type': 'divider'}, {'type': 'actions', 'elements': [{'type': 'button', 'text': {'type': 'plain_text', 'text': 'Farmhouse', 'emoji': True}, 'value': 'click_me_123'}, {'type': 'button', 'text': {'type': 'plain_text', 'text': 'Kin Khao', 'emoji': True}, 'value': 'click_me_123', 'url': 'https://google.com'}, {'type': 'button', 'text': {'type': 'plain_text', 'text': 'Ler Ros', 'emoji': True}, 'value': 'click_me_123', 'url': 'https://google.com'}]}]}

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

@app.route('/', methods=['GET', 'POST'])
def lambda_handler(event=None, context=None):
    
    logger.info('Lambda function invoked index()')

    print(f"Received event:\n{event}\nWith context:\n{context}")

    try:
        print(event.keys())
        narrowed_down_text = event['body']
        print(f"Somewhere in here is the slack input text: {narrowed_down_text}")
    except:
        print('Lambda function inputs not as expected. Probably called from different access point')
    
    return {
        "statusCode": 200,
        "body": json.dumps(payload),
    }

if __name__ == '__main__':
    app.run(debug=True)
