#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013-2014 Tribus Developers
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

from celery import task
from fabric.api import execute, env, sudo, local
from tribus.common.fabric.consul import deploy_test_service


@task
def queue_service_deploy(*args):
    env.port = 22
    env.user = args[0]['user']
    env.password = args[0]['pw']
    env.host_string = local('echo $HOST_DIR', capture=True)
    env.service_name = args[0]['name']
    execute(deploy_test_service)
