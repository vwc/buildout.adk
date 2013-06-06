from __future__ import with_statement
from fabric.api import cd
from fabric.api import env
from fabric.api import local
from fabric.api import run
from fabric.api import sudo


def live():
    env.use_ssh_config = True
    env.forward_agent = True
    env.port = '22222'
    env.user = 'root'
    env.hosts = ['6zu4']
    env.webserver = '/opt/webserver/buildout.webserver'
    env.code_root = '/opt/sites/adk-staging/buildout.adk'
    env.sitename = 'adk'
    env.code_user = 'root'
    env.prod_user = 'www'


def ls():
    with cd(env.code_root):
        run('ls')


def server_uptime():
    run('uptime')


def server_load():
    run('cat /proc/loadavg')


def server_memory():
    run('free')


def server_filesystem():
    run('df -ha')


def status():
    """
        Find out the running status of the server and deploy.
    """
    # General health of the server.
    server_uptime()
    server_load()
    server_memory()
    server_filesystem()
    with cd(env.webserver):
        run('bin/supervisorctl status')


def update():
    with cd(env.code_root):
        run('nice git pull')


def rebuild():
    with cd(env.code_root):
        run('bin/buildout -Nc deployment.cfg')


def instance_restart():
    with cd(env.webserver):
        run('nice bin/supervisorctl restart instance-%(sitename)s' % env)


def supervisorctl(*cmd):
    """Runs an arbitrary supervisorctl command."""
    with cd(env.webserver):
        run('bin/supervisorctl ' + ' '.join(cmd))


def deploy():
    update()
    #rebuild()
    instance_restart()
