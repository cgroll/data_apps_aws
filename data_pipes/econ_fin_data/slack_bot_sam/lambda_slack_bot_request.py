import json

def lambda_handler(event, context):
    print(f"Received event:\n{event}\nWith context:\n{context}")
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "text": 'Here is a link: <[https://youtu.be/frszEJb0aOo|General Kenobi!>. :smile: This is a text with `inline *code*` in it.\n- water\n- bread\n - salt,',
            "message": 'HELLO WORLD',
        }),
    }
