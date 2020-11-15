import os
from string import Template
from config import *

template_dir = TEMPLATE_DIR

def render_template(path, replacements={}):
    f = open(os.path.join(template_dir, path))
    s = f.read()
    f.close()

    return Template(s).safe_substitute(replacements)

def redirect(page):
    return render_template('redirect.html', {'page': page})
