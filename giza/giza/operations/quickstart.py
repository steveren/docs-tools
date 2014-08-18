# Copyright 2014 MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os
import inspect
import shutil

logger = logging.getLogger('giza.operations.quickstart')

import argh
import giza

from giza.command import command, CommandError
from giza.config.helper import fetch_config
from giza.operations.sphinx import sphinx_publication
from giza.app import BuildApp

@argh.named('quickstart')
def make_project(args):
    curdir = os.getcwd()
    curdir_list = os.listdir(curdir)

    if len(curdir_list) > 0 and (not len(curdir_list) == 1 and not '.git' in curdir_list):
        logger.critical('cannot create new project in directory that already has files: ' + curdir)
        _weak_bootstrapping(args)
        logger.info('attempted to bootstrap buildsystem')
    else:
        mod_path = os.path.dirname(inspect.getfile(giza))
        qstart_path = os.path.join(mod_path, 'quickstart')

        command('rsync -r {0}/. {1}'.format(qstart_path, curdir))
        command('git init')
        command('git add .')
        try:
            command('git commit -m "initial commit"')
        except CommandError:
            pass

        logger.info('created project skeleton in current directory.')

        _weak_bootstrapping(args)

def _weak_bootstrapping(args):
    conf = fetch_config(args)
    app = BuildApp(conf)

    try:
        sphinx_publication(conf, args, app)
    except:
        sphinx_publication(conf, args, app)
        shutil.rmtree('docs-tools')

    command('python build/docs-tools/makecloth/meta.py build/makefile.meta')
