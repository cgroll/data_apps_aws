import os
from data_apps_aws.nb_render import render_nb
from data_apps_aws.slack_bots import slack_rendering_error, jupyter_status_update

notebook_list = ['index',
                 'macro_econ_release_data'
                 ]

def download_render_upload_notebook(nb_name_no_extension):
    # Download notebook to be rendered
    fname = 'https://raw.githubusercontent.com/cgroll/data_apps_aws/master/notebooks/' + nb_name_no_extension + '.ipynb'
    local_name = nb_name_no_extension + '.ipynb'

    cmd_str = f'curl -o {local_name} {fname}'
    os.system(cmd_str)


    # Download template file that defines rendering output
    tpl_name = 'jupyter_hide_code_export.tpl'
    fname = 'https://raw.githubusercontent.com/cgroll/data_apps_aws/master/api_landing_page/' + tpl_name

    cmd_str = f'curl -o {tpl_name} {fname}'
    os.system(cmd_str)


    # render the notebook locally
    render_nb(local_name, './output/', nb_name_no_extension)

    # upload notebook to s3
    html_out_name = nb_name_no_extension + '.html'
    local_html_out_path = './output/' + html_out_name

    # Note: use AWS client. With Boto3 the file metadata did get screwed
    aws_cli_cmd = f'aws s3 cp {local_html_out_path} s3://notebook-html-file-server/'
    os.system(aws_cli_cmd)


for this_nb in notebook_list:

    try:
        print(f'Rendering {this_nb}')
        download_render_upload_notebook(this_nb)
        print(f'Rendering successful')
        jupyter_status_update(this_nb)
        
    except:
        print('Rending not successful')
        slack_rendering_error(this_nb)

