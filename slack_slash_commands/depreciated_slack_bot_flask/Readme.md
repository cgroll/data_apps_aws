## Take-aways

AWS lambda functions have a specific interfaces: they get called with
an event and a context input. Flask, however, generally requires a
different interface to API calls: it receives GET and POST requests.
Hence, in order to wrap a flask app into a AWS lambda function we
somehow need to have another interface between flask and AWS lambda in
order to translate AWS lambda events to flask compatible requests.

I had a hard time figuring out how the returned function values would
need to look like that they comply with slack formatting after
returning them through the AWS lambda interface.

Besides that, some features seemed really nice:

- easy deployment
- automatically adds a scheduled event bridge to the AWS lambda
  function in order to avoid cold start problem
- flask would be a more powerful / general way of developing a web app


## Zappa commands

```
zappa deploy
zappa update prod
zappa invoke prod 'app.lambda_handler'
zappa undeploy
```
