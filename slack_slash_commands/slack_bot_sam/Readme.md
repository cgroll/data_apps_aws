## Requirements

- specify all requirements in requirements.txt, including the
  requirements from the data_apps_aws package itself
- add the data_apps_aws wheel file (without dependencies) to the
  requirements

Note: in order to deploy changes to lambda that also require changes
in the core package then the package needs to be re-deployed to get an
up to date wheel file!

## Infrastructure resources:

https://medium.com/decentlabs/making-a-message-replacing-slash-command-slack-bot-using-aws-lambda-api-gateway-98e5d8e17a4c

- API Gateway setup: checking the **Use Lambda Proxy integration** for
  POST method! This means that the full original request will be
  proxied from API Gateway to Lambda. Without it, API Gateway grabs
  the original request, handles it, and sends a different request
  (with stripped down data) over to Lambda.
- special case: replacing an existing message instead of just
  responding in a new message
- Deal with long-running requests: The first line in the handler is
  our “immediate response” of an empty 200 response. Slack asks us to
  provide this to acknowledge that we’ll be handling this request
  eventually (in a new request, which we’ll build up manually). 
- based on Javascript example

https://codeburst.io/building-a-slack-slash-bot-with-aws-lambda-python-d0d4a400de37

- base64 encoding
- urlencoding
- ascii


https://medium.com/glasswall-engineering/how-to-create-a-slack-bot-using-aws-lambda-in-1-hour-1dbc1b6f021c

- urlencoding
- ascii
- respond through additional web hook, not through regular function
  output 


https://medium.com/swlh/slack-slash-command-integration-with-aws-lambda-c7f2c4f2e076

- two layers of lambda functions
- deal with Slack's 3s timeout
- API	authentication

## Slack frontend resources

- [Slack Block Kit Builder](https://app.slack.com/block-kit-builder)
- some examples and specifications of rich output: https://api.slack.com/changelog/2019-09-what-they-see-is-what-you-get-and-more-and-less

