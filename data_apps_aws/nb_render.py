import re

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError
from nbconvert import HTMLExporter
from traitlets.config import Config
from nbconvert.writers import FilesWriter

def scrape_original_trace(trace):
    ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -/]*[@-~]')
    trace = ansi_escape.sub('', trace)

    match = re.search(r'(?<=------------------\n\n).+', trace, re.DOTALL)
    return match.group(0) if match else trace

def render_nb(nb_name, output_path, jpynb_output_name, tpl_name='./jupyter_hide_code_export.tpl'):

    try:

        # executing the notebook
        ep = ExecutePreprocessor(timeout=900)
        nb = nbformat.read(nb_name, nbformat.NO_CONVERT)
        (nb, resources) = ep.preprocess(nb, resources=dict())

        # transforming it to html
        html_exporter = HTMLExporter()
        html_exporter.template_file = tpl_name
        (body, resources) = html_exporter.from_notebook_node(nb, resources)

        # write it to a file
        c = Config()
        c.FilesWriter.build_directory = output_path
        fw = FilesWriter(config=c)
        fw.write(body, resources, notebook_name=jpynb_output_name)

    except Exception as e:

        print(f"Exception while rendering {nb_name}:")
        error_msg = scrape_original_trace(e.traceback)
        # print(e.traceback)
        print(error_msg)
        # rethrow_error = True
