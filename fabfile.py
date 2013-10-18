import os

from fabric.api import *
from fabric.decorators import roles

env.roledefs.update({
    'dev_server': ['ubuntu@precise.dev.unomena.net'],
    'qa_server': ['ubuntu@precise.qa.unomena.net'],
    'prod_servers': ['ubuntu@web1.prod.unomena.net', 'ubuntu@web2.prod.unomena.net']
})

REPO_PATH = 'unomena-starter'
PROJECT_NAME = 'unomena-starter'

def build_project(where, code_dir=os.path.dirname(__file__)):
    assert where in ['local', 'remote'], "invalid option to where"
    
    if where == 'local':
        run_func = local
    elif where == 'remote':
        run_func = run
    
    with cd(code_dir):
        run_func('python bootstrap.py')
        run_func('bin/buildout')

def prepare_deploy():
    local('git add . && git commit')
    local('git push')
    
def test_repo_exists(code_dir):
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@git.unomena.net:%s.git %s" % (REPO_PATH, code_dir))

def deploy():
    run('git pull')

@roles('dev_server')
def deploy_dev():
    code_dir = '/home/ubuntu/dev/%s' % PROJECT_NAME
    
    test_repo_exists(code_dir)
    
    with cd(code_dir):
        deploy()
        