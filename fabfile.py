from fabric.api import run,local,cd,env
import config

try:
    from fab_config import *
except ImportError:
    pass
    #abort("I haz no config options !")

# fab_config.py should contain something like this :

# from fabric.api import env
# env.roledefs = {
#     'test': ['localhost'],
#     'dev': ['user@dev.example.com'],
#     'staging': ['user@staging.example.com'],
#     'production': ['user@production.example.com']
# }
# DISTANT_PATH = '/path/to/your/code/'
# PROCESSES = ['bouncy-web','bouncy-convert']

def pull():
    with cd(DISTANT_PATH):
        run('git pull')

def push():
    local("git push")

def restart_services():
    run('sudo supervisorctl restart' + PROCESSES.join(' '))

def deploy():
    pull()
    restart_services()

def full_deploy():
    push()
    deploy()

def empty_tmp():
    run('rm -r {}'.format(config.PROCESSING_DIR))
    run('mkdir {}'.format(config.PROCESSING_DIR))