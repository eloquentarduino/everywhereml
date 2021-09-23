import re
import os.path
from os import getcwd
from os import makedirs
from glob import glob
from subprocess import check_output, STDOUT
from bs4 import BeautifulSoup
from multiprocessing import Pool


def process(notebook):
    base_dir = '/Users/simone/WebstormProjects/everywheremldocs/src'
    base_html_dir = os.path.join(base_dir, '.vuepress/public/notebooks')
    base_md_dir = os.path.join(base_dir, 'documentation/notebooks')

    print('Processing...', notebook)
    notebook_dir = os.path.dirname(notebook).replace('docs/', '')
    cmd = ['jupyter', 'nbconvert', '--to', 'html', '--output-dir', getcwd(), '--output', 'notebook.html', notebook]
    output = check_output(cmd, stderr=STDOUT).decode('utf-8')

    if 'Writing' not in output:
        print('Error on', notebook)
        return False

    with open('notebook.html', encoding='utf-8') as file:
        dom = BeautifulSoup(file.read(), 'lxml')
        html = str(dom.body).replace('body', 'div')
        html = re.sub(r'<h1.+?</h1>', '', html)

    filename = os.path.basename(notebook).replace('.ipynb', '')
    html_output_dir = os.path.join(base_html_dir, notebook_dir)
    md_output_dir = os.path.join(base_md_dir, notebook_dir)

    if not os.path.isdir(html_output_dir):
        makedirs(html_output_dir, 0o777)

    if not os.path.isdir(md_output_dir):
        makedirs(md_output_dir, 0o777)

    with open(os.path.join(html_output_dir, '%s.html' % filename), 'w', encoding='utf-8') as file:
        file.write(html)

    with open(os.path.join(md_output_dir, '%s.md' % filename), 'w', encoding='utf-8') as file:
        title = filename
        path = os.path.join(notebook_dir, filename)
        file.write('''
# %s

<div id="notebook-container"></div>
<script>
    fetch('/notebooks/%s.html').then(res => res.text()).then(html => document.getElementById('notebook-container').innerHTML = html)
</script>
                ''' % (title, path))

    return True


if __name__ == '__main__':
    with Pool(1) as pool:
        notebooks = sorted(glob('docs/**/*.ipynb', recursive=True))
        pool.map(process, notebooks)
