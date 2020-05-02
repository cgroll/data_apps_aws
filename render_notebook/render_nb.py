import os
from data_apps_aws.nb_render import render_nb

# Download notebook to be rendered
nb_name = 'index'
fname = 'https://raw.githubusercontent.com/cgroll/data_apps_aws/master/notebooks/' + nb_name + '.ipynb'
local_name = nb_name + '.ipynb'
out_name = nb_name

cmd_str = f'curl -o {local_name} {fname}'
os.system(cmd_str)


# Download template file that defines rendering output
tpl_name = 'jupyter_hide_code_export.tpl'
fname = 'https://raw.githubusercontent.com/cgroll/data_apps_aws/master/api_landing_page/' + tpl_name

cmd_str = f'curl -o {tpl_name} {fname}'
os.system(cmd_str)


# render the notebook locally
render_nb(local_name, './output/', out_name)


# upload notebook to s3
html_out_name = out_name + '.html'
local_html_out_path = './output/' + html_out_name

# Note: use AWS client. With Boto3 the file metadata did get screwed
aws_cli_cmd = f'aws s3 cp {local_html_out_path} s3://notebook-html-file-server/'
os.system(aws_cli_cmd)
