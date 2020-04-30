from data_apps_aws.src.nb_render import render_nb

if __name__ == "__main__":
    render_nb('api_gateway_page.ipynb', './output/',
              'api_gateway_page',
              tpl_name='./jupyter_hide_code_export.tpl'
    )
