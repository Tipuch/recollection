from __future__ import with_statement
import os
from fabric.api import cd, prefix, run, env


env.hosts = ['tipuch@158.69.206.24']
base_dir = "/home/tipuch"
working_dir = os.path.join(base_dir, "projects/recollection/")
virtual_env = os.path.join(base_dir, "virtualenvs/recollection_env/bin/")
uwsgi_ini = "recollection.ini"


def deploy():
    with cd(working_dir):
        with prefix("source %sactivate" % virtual_env):
            run("git pull origin master")
            run("pip install -Ur requirements.txt")
            run("python manage.py collectstatic --noinput")
            run("python manage.py migrate")
            run("touch %s" % uwsgi_ini)
            run("python manage.py test")
