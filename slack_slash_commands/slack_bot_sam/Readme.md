# Requirements

- specify all requirements in requirements.txt, including the
  requirements from the data_apps_aws package itself
- add the data_apps_aws wheel file (without dependencies) to the
  requirements

## Resources:

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
