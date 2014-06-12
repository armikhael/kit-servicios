#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Desarrolladores de Tribus
#
# This file is part of Tribus.
#
# Tribus is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tribus is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from fabric.api import local
from tribus.common.fabric.maint import docker_kill_all_containers


def django_syncdb(env):
    '''
    '''

    docker_kill_all_containers(env)
    local(('echo "#!/usr/bin/env python\n'
           'import subprocess\n'
           'from django.core import management\n'
           'from django.contrib.auth.models import User\n'
           'from tribus.web.registration.ldap.utils import create_ldap_user\n'
           '%(restart_services_python)s\n'
           'management.call_command(\'syncdb\', interactive=False)\n'
           'management.call_command(\'migrate\', interactive=False)\n'
           'su_data = [\'tribus\', \'tribus@localhost.com\', \'tribus\']\n'
           'su = User.objects.create_superuser(*su_data)\n'
           'create_ldap_user(su)\n'
           '" > %(tribus_django_syncdb_script)s') % env, capture=False)
    local(('sudo bash -c '
           '"%(docker)s run -it --name="%(tribus_runtime_container)s" '
           '%(preseed_env)s %(mounts)s %(tribus_runtime_image)s '
           'python %(tribus_django_syncdb_script)s"') % env)
    local(('sudo bash -c '
           '"%(docker)s commit %(tribus_runtime_container)s '
           '%(tribus_runtime_image)s"') % env)


def django_runserver(env):
    '''
    '''

    docker_kill_all_containers(env)
    local(('echo "'
           'upstream uwsgi {\n'
           '\tserver\t\t\t\tunix:///var/run/tribus/uwsgi.sock;\n'
           '}\n'
           '\n'
           'server {\n'
           '\tlisten\t\t\t\t8000;\n'
           '\tserver_name\t\t\t127.0.0.1;\n'
           '\tcharset\t\t\t\tutf-8;\n'
           '\n'
           '\tlocation /static {\n'
           '\t\talias\t\t\t%(tribus_static_dir)s;\n'
           '\t}\n'
           '\n'
           '\tlocation / {\n'
           '\t\tuwsgi_pass\t\tuwsgi;\n'
           '\t\tinclude\t\t\t/etc/nginx/uwsgi_params;\n'
           '\t}\n'
           '}'
           '" > %(tribus_nginx_config)s') % env, capture=False)
    local(('echo "'
           '[program:tribus-celery]\n'
           'command=/usr/bin/python %(basedir)s/manage.py celeryd\n'
           'directory=%(basedir)s\n'
           'user=www-data\n'
           'numprocs=1\n'
           'stdout_logfile=/var/log/tribus/celeryd.log\n'
           'stderr_logfile=/var/log/tribus/celeryd.log\n'
           'autostart=true\n'
           'autorestart=true\n'
           'startsecs=10\n'
           'stopwaitsecs=30\n'
           '\n'
           '[program:tribus-celerybeat]\n'
           'command=/usr/bin/python %(basedir)s/manage.py celerybeat\n'
           'directory=%(basedir)s\n'
           'user=www-data\n'
           'numprocs=1\n'
           'stdout_logfile=/var/log/tribus/celerybeat.log\n'
           'stderr_logfile=/var/log/tribus/celerybeat.log\n'
           'autostart=true\n'
           'autorestart=true\n'
           'startsecs=10\n'
           'stopwaitsecs=30\n'
           '" > %(tribus_supervisor_config)s') % env, capture=False)
    local(('echo "'
           '[uwsgi]\n'
           'chdir           = %(basedir)s\n'
           'env             = DJANGO_SETTINGS_MODULE=tribus.config.web\n'
           'wsgi-file       = %(basedir)s/tribus/web/wsgi.py\n'
           'logto           = /var/log/tribus/uwsgi.log\n'
           'pidfile         = /var/run/tribus/uwsgi.pid\n'
           'socket          = /var/run/tribus/uwsgi.sock\n'
           'plugin          = python\n'
           '" > %(tribus_uwsgi_config)s') % env, capture=False)
    local(('echo "#!/usr/bin/env bash\n'
           'ln -fs /proc/self/fd /dev/fd\n'
           'ln -fs %(tribus_nginx_config)s /etc/nginx/sites-enabled/\n'
           'ln -fs %(tribus_uwsgi_config)s /etc/uwsgi/apps-enabled/\n'
           'ln -fs %(tribus_supervisor_config)s /etc/supervisor/conf.d/\n'
           '%(restart_services)s\n'
           'sleep 1200\n'
           'exit 0'
           '" > %(tribus_django_runserver_script)s') % env, capture=False)
    local(('sudo bash -c '
           '"%(docker)s run -d -p 127.0.0.1:8000:8000 '
           '--name="%(tribus_runtime_container)s" '
           '%(preseed_env)s %(mounts)s %(tribus_runtime_image)s '
           'bash %(tribus_django_runserver_script)s"') % env)
