from fabric.api import local, task, abort, settings
from clom import clom
from fabric.colors import green
from fabric.utils import puts
from fabric.operations import prompt

@task
def release():
    """
    Release current version to pypi
    """    

    with settings(warn_only=True):
        r = local(clom.git['diff-files']('--quiet', '--ignore-submodules', '--'))

    if r.return_code != 0:
        abort('There are uncommitted changes, commit or stash them before releasing')

    version = open('VERSION.txt').read().strip()

    puts(green('Releasing %s...' % version))
    local(clom.git.flow.release.start(version))

    # Can't use spaces in git flow release messages, see https://github.com/nvie/gitflow/issues/98
    local(clom.git.flow.release.finish(version, m='Release-%s' % version))

    if prompt('Push to origin?'):
        local(clom.git.push('origin', 'master', 'develop').with_opts(tags=True))        

        if prompt('Push to pypi?'):
            local(clom.python('setup.py', 'sdist', 'upload'))

@task
def register():
    """
    Register current version to pypi
    """
    local(clom.python('setup.py', 'register'))    