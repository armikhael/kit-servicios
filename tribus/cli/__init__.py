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

"""

This is the Tribus module where all command line functions reside.

This module contains funtions to provide the same functionality of the web
interface but through the console.

"""

import json
from tribus import BASEDIR
from fabric.api import run, env, settings, sudo, hide, put, cd, local, quiet
from tribus.common.utils import get_path
from tribus.common.fabric.development import docker_create_service_cluster
from tribus.common.logger import get_logger

log = get_logger()

env.host = 'localhost'
env.port = '22'

def servicios():
	"""Lista los servicios disponibles en kit de servicios"""
	return "Lista de servicios"


