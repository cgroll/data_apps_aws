from slackbot.bot import listen_to

@listen_to('Hi')
def hello(message):
    message.send('Hi :beer:')
