import os
from string import Template
from config import *

template_dir = TEMPLATE_DIR
copyright = '''
<footer>
    <p class="has-text-centered has-text-grey-light"><small>Copyright &copy; 2020 Christopher Liu. All rights reserved.</small></p>
</footer>
'''

def render_template(path, replacements={}):
    f = open(os.path.join(template_dir, path))
    s = f.read()
    f.close()

    return Template(s).safe_substitute(replacements) + copyright

def redirect(page):
    return render_template('redirect.html', {'page': page}) + copyright
