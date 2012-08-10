# Copyright European Organization for Nuclear Research (CERN)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Authors:
# - Vincent Garonne, <vincent.garonne@cern.ch>, 2011-2012
# - Mario Lassnig, <mario.lassnig@cern.ch>, 2012

import glob
import shutil
import os
import re
import subprocess
import sys

#from distutils.core import Command
from distutils.command.sdist import sdist as _sdist
#from distutils.command.build import build as _build

if sys.version_info < (2, 4):
    print('ERROR: Rucio requires at least Python 2.5 to run.')
    sys.exit(1)

sys.path.insert(0, os.path.abspath('lib/'))

from rucio import version

try:
    from setuptools import setup, find_packages
#    from setuptools.command.sdist import sdist
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

name = 'rucio'
packages = find_packages('lib/')
description = "Rucio Package"
IsRelease = False
requirements_files = ['tools/pip-requires', 'tools/pip-requires-client']
data_files = [('etc/', glob.glob('etc/*.template')),
              ('etc/web', glob.glob('etc/web/*.template')),
              ('tools/', glob.glob('tools/*'))]

# Arguments to the setup script to build Basic/Lite distributions
copy_args = sys.argv[1:]
if '--client' in copy_args:
    name = 'rucio-clients'
    packages = ['rucio', 'rucio.client', 'rucio.common', 'rucio.client.api', 'rucio.rse.protocols', 'rucio.client.api.rse']
    requirements_files = ['tools/pip-requires-client']
    description = "Rucio Client Lite Package"
    data_files = [('etc/', ['etc/rse-accounts.cfg.template', 'etc/rucio.cfg.template']),
                  ('tools/', ['tools/pip-requires-client', ]), ]
    if os.path.exists('build/'):
        shutil.rmtree('build/')
    if os.path.exists('lib/rucio_clients.egg-info/'):
        shutil.rmtree('lib/rucio_clients.egg-info/')
    if os.path.exists('lib/rucio.egg-info/'):
        shutil.rmtree('lib/rucio.egg-info/')
    copy_args.remove('--client')

if '--release' in copy_args:
    IsRelease = True
    copy_args.remove('--release')


def run_git_command(cmd):
    output = subprocess.Popen(["/bin/sh", "-c", cmd],
                              stdout=subprocess.PIPE)
    return output.communicate()[0].strip()


if os.path.isdir('.git'):
    if IsRelease:
        git_version_cmd = 'git describe --abbrev=4'
    else:
        #git_version_cmd = '''git describe --long --dirty="-`date +%s`"| sed 's/.*\([-][0-9][0-9]*[-][a-z0-9]*\)/\1/' '''
        git_version_cmd = '''git describe --dirty=-dev`date +%s`'''
    git_version = run_git_command(git_version_cmd)
    branch_nick_cmd = 'git branch | grep -Ei "\* (.*)" | cut -f2 -d" "'
    branch_nick = run_git_command(branch_nick_cmd)
    revid_cmd = "git rev-parse HEAD"
    revid = run_git_command(revid_cmd)
    revno_cmd = "git --no-pager log --oneline | wc -l"
    revno = run_git_command(revno_cmd)
    version_file = open("lib/rucio/vcsversion.py", 'w')
    version_file.write("""
# This file is automatically generated by setup.py, So don't edit it. :)
version_info = {
    'final': %s,
    'version': '%s',
    'branch_nick': '%s',
    'revision_id': '%s',
    'revno': %s
}
""" % (IsRelease, git_version, branch_nick, revid, revno))
    version_file.close()

# If Sphinx is installed on the box running setup.py,
# enable setup.py to build the documentation, otherwise,
# just ignore it
cmdclass = {}

try:
    from sphinx.setup_command import BuildDoc

    class local_BuildDoc(BuildDoc):
        def run(self):
            for builder in ['html']:   # 'man','latex'
                self.builder = builder
                self.finalize_options()
                BuildDoc.run(self)
    cmdclass['build_sphinx'] = local_BuildDoc
except:
    pass


def get_reqs_from_file(requirements_file):
    if os.path.exists(requirements_file):
        return open(requirements_file, 'r').read().split('\n')
    return []


def parse_requirements(requirements_files):
    requirements = []
    for requirements_file in requirements_files:
        for line in get_reqs_from_file(requirements_file):
            if re.match(r'\s*-e\s+', line):
                requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
            elif re.match(r'\s*-f\s+', line):
                pass
            else:
                requirements.append(line)
    return requirements


def parse_dependency_links(requirements_files):
    dependency_links = []
    for requirements_file in requirements_files:
        for line in get_reqs_from_file(requirements_file):
            if re.match(r'(\s*#)|(\s*$)', line):
                continue
            if re.match(r'\s*-[ef]\s+', line):
                dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))
    return dependency_links


def write_requirements():
    venv = os.environ.get('VIRTUAL_ENV', None)
    if venv is not None:
        with open("requirements.txt", "w") as req_file:
            output = subprocess.Popen(["pip", "freeze", "-l"],
                                      stdout=subprocess.PIPE)
            requirements = output.communicate()[0].strip()
            req_file.write(requirements)

requires = parse_requirements(requirements_files=requirements_files)
depend_links = parse_dependency_links(requirements_files=requirements_files)
#write_requirements()


class CustomSdist(_sdist):

    user_options = [
        ('packaging=', None, "Some option to indicate what should be packaged")
    ] + _sdist.user_options

    def __init__(self, *args, **kwargs):
        _sdist.__init__(self, *args, **kwargs)
        self.packaging = "default value for this option"

    def get_file_list(self):
        print "Chosen packaging option: " + name
        self.distribution.data_files = data_files
        _sdist.get_file_list(self)

    #def make_release_tree(self, base_dir, files):
    #    _sdist.make_release_tree(self, base_dir, files)
    #    print 'make_release_tree', base_dir, files


    #def make_distribution(self):
    #    _sdist.make_distribution(self)
    #    print '_sdist.make_distribution'


cmdclass['sdist'] = CustomSdist

setup(
    name=name,
    version=version.version_string(),
    packages=packages,
    package_dir={'': 'lib'},
    data_files=data_files,
    script_args=copy_args,
    cmdclass=cmdclass,
    include_package_data=True,
    scripts=['bin/rucio', 'bin/rucio-admin'],
    # doc=cmdclass,
    author="Vincent Garonne",
    author_email="vincent.garonne@cern.ch",
    description=description,
    license="Apache License, Version 2.0",
    url="http://rucio.cern.ch/",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Environment :: No Input/Output (Daemon)', ],
    install_requires=requires,
    dependency_links=depend_links,
)
