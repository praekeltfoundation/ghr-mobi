import os

import getpass

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from fabric.api import *
from fabric.decorators import roles

APP_NAME = 'unomena'
REPO_PATH = 'unomena/unomena-starter'
PROJECT_NAME = 'unomena-starter'
IN_HOUSE_DOMAIN = 'unomena.net'
FRONTEND_PROXY_PORT = '12000'
HTTPS_PORT = '443'
PRODUCTION_SERVER_NAME = 'unomena-starter.com'
DEPLOY_USER = getpass.getuser()

env.roledefs.update({
    'dev_server': ['ubuntu@precise.dev.unomena.net'],
    'qa_server': ['ubuntu@precise.qa.unomena.net'],
    'prod_servers': ['ubuntu@web1.prod.unomena.net', 'ubuntu@web2.prod.unomena.net']
})

buildout_config = {
    'project_name': PROJECT_NAME,
    'frontend_proxy_port': FRONTEND_PROXY_PORT,
    'https_port': HTTPS_PORT,
    'app_name': APP_NAME
}

def email_project_deployed(instance_type):
    fromaddr = "Unomena <unomena.com>"
    toaddr = "dev@unomena.com"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "[Deploy] [%s] instance %s by %s" % (PROJECT_NAME, instance_type, DEPLOY_USER)
     
    body = """
    This is an automated email from the deployment script. It was
    generated because the project "%s" was deployed.
     
    Instance: %s
     
    Deployed by: %s
    """ % (PROJECT_NAME, instance_type, DEPLOY_USER)
     
    msg.attach(MIMEText(body, 'plain'))
     
    try:
        smtp_obj = smtplib.SMTP('mail.unomena.net')
        smtp_obj.login('mailman', 'AKmiQldQ2e')
        smtp_obj.sendmail(fromaddr, toaddr, msg.as_string())  
    except Exception, exc:
        pass

def build_project(where, instance_type='dev', 
                  nginx_conf_changed=False, code_dir='.'):
    assert where in ['local', 'remote'], "invalid option to where"
    
    if where == 'local':
        run_func = local
    elif where == 'remote':
        run_func = run
    
    if instance_type == 'master':
        server_name = PRODUCTION_SERVER_NAME
    else:
        server_name = '%s.%s.%s' % (PROJECT_NAME, instance_type, IN_HOUSE_DOMAIN)
        
    buildout_config.update({
        'server_name': server_name
    })
    
    with cd(code_dir):
        run_func('python bootstrap.py')
        run_func(
            'bin/buildout buildout:server-names="%(server_name)s" '
            'buildout:server-name="%(server_name)s" '
            'buildout:app-name="%(app_name)s" '
            'buildout:frontend-proxy-port="%(frontend_proxy_port)s" '
            'buildout:https-port="%(https_port)s"'
            % buildout_config
        )
        
        if where == 'remote':
            # chowns
            run_func('sudo chown -R ubuntu:unoweb bin')
            run_func('sudo chown ubuntu:unoweb logs')
            run_func('sudo chown ubuntu:unoweb scheduler')
            run_func('sudo chown ubuntu:unoweb static')
            run_func('sudo chown ubuntu:unoweb media')
            
            # sticky bits
            run_func('sudo chmod g+s bin')
            run_func('sudo chmod g+s logs')
            run_func('sudo chmod g+s scheduler')
            run_func('sudo chmod g+s static')
            run_func('sudo chmod g+s media')
            
            # chmods
            run_func('sudo chmod -R 770 bin')
            run_func('sudo chmod 764 logs')
            run_func('sudo chmod 660 .installed.cfg')
            run_func('sudo chmod 760 scheduler')
            run_func('sudo chmod 644 static')
            run_func('sudo chmod 764 media')
            
            # mkdirs
            with settings(warn_only=True):
                if run_func("test -d media/uploads").failed:
                    run_func('mkdir media/uploads')
                    
                if run_func("test -d src/project/settings_local.py").failed:
                    run_func('touch src/project/settings_local.py')
                    run_func("echo -e 'DEBUG = True\nTEMPLATE_DEBUG = DEBUG' > src/project/settings_local.py")
        
            if nginx_conf_changed:
                # symlink nginx
                with settings(warn_only=True):
                    run_func('sudo rm /etc/nginx/sites-available/%s' % server_name)
                    run_func('sudo ln -s $PWD/nginx/%s.conf /etc/nginx/sites-available/%s.conf' % (server_name, server_name))
                    run_func('sudo rm /etc/nginx/sites-enabled/%s' % server_name)
                    run_func('sudo ln -s $PWD/nginx/%s.conf /etc/nginx/sites-enabled/%s.conf' % (server_name, server_name))
            
            with settings(warn_only=True):
                # symlink supervisor gunicorn
                run_func('sudo rm /etc/supervisor/conf.d/%s.gunicorn.conf' % server_name)
                run_func('sudo ln -s $PWD/supervisor/gunicorn.conf /etc/supervisor/conf.d/%s.gunicorn.conf' % server_name)
                
                # symlink supervisor celeryd
                run_func('sudo rm /etc/supervisor/conf.d/%s.celeryd.conf' % server_name)
                run_func('sudo ln -s $PWD/supervisor/celeryd.conf /etc/supervisor/conf.d/%s.celeryd.conf' % server_name)
    
            # restart supervisor processes
            run_func('sudo supervisorctl restart %s.gunicorn' % server_name)
            run_func('sudo supervisorctl restart %s.celeryd' % server_name)
            if nginx_conf_changed:
                run_func('bin/make_cert.sh')
                run_func('sudo service nginx restart')
        
        # restart memcached
        run_func('sudo service memcached restart')
        
        # sync db
        run_func('bin/django syncdb')
        
        # run migrations
        run_func('bin/django migrate')
        
def prepare_deploy():
    local('git add . && git commit')
    local('git push')

@roles('dev_server')
def test_db_exists(db_name):
    with settings(warn_only=True):
        print run("psql -l | grep %s | wc -l" % db_name)
        #    run("git clone git@git.unomena.net:%s.git %s" % (REPO_PATH, code_dir))
    #email_project_deployed('dev')
    
def test_repo_exists(code_dir):
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git@git.unomena.net:%s.git %s" % (REPO_PATH, code_dir))

def deploy(instance_type, code_dir):
    run('git checkout %s' % instance_type)
    run('git pull origin %s' % instance_type)
    
    # todo: git diff code to determine if nginx conf changed
    # git diff HEAD:full/path/to/foo full/path/to/bar
    
    build_project('remote', instance_type, True, code_dir)
    
    email_project_deployed(instance_type)

@roles('dev_server')
def deploy_dev():
    code_dir = '/home/ubuntu/dev/%s' % PROJECT_NAME
    instance_type = 'master'
    
    test_repo_exists(code_dir)
    
    with cd(code_dir):
        deploy(instance_type, code_dir)
        
@roles('qa_server')
def deploy_qa():
    code_dir = '/home/ubuntu/qa/%s' % PROJECT_NAME
    instance_type = 'qa'
    
    test_repo_exists(code_dir)
    
    with cd(code_dir):
        deploy(instance_type, code_dir)
        
@roles('prod_servers')
def deploy_prod():
    code_dir = '/var/www/%s' % PROJECT_NAME
    instance_type = 'master'
    
    test_repo_exists(code_dir)
    
    with cd(code_dir):
        deploy(instance_type, code_dir)
        