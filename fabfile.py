import os

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

from fabric.api import *
from fabric.decorators import roles

from fab_settings import *

env.roledefs.update({
    'dev_server': DEV_SERVERS,
    'qa_server': QA_SERVERS,
    'prod_servers': PROD_SERVERS
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
            run_func('sudo chmod 774 logs')
            run_func('sudo chmod 660 .installed.cfg')
            run_func('sudo chmod 760 scheduler')
            run_func('sudo chmod 644 static')
            run_func('sudo chmod 774 media')
            
            # mkdirs
            with settings(warn_only=True):
                if run_func("test -d media/uploads").failed:
                    run_func('mkdir media/uploads')
                    
                if run_func("test -d src/project/settings_local.py").failed:
                    run_func('touch src/project/settings_local.py')
                    
                    debug_string = 'DEBUG = %s' % instance_type == 'prod' \
                        and 'False' or 'True'
                    template_debug_string = 'TEMPLATE_DEBUG = DEBUG'
                    settings_dict = {
                        'engine': 'django.db.backends.postgresql_psycopg2',
                        'name': instance_type in ['dev', 'qa'] and '%s_%s' \
                            % (PROJECT_NAME, instance_type) or PROJECT_NAME,
                        'user': PROJECT_NAME,
                        'password': PROJECT_NAME,
                        'host': 'localhost',
                        'port': '5432'        
                    }
                    settings_string = (
                        "DATABASES = {\n"
                        "    'default': {\n"
                        "        'ENGINE': '%(engine)s',\n"
                        "        'NAME': '%(name)s',\n"
                        "        'USER': '%(user)s',\n"
                        "        'PASSWORD': '%(password)s',\n"
                        "        'HOST': '%(host)s',\n"
                        "        'PORT': '%(port)s',\n"
                        "    }\n"
                        "}" % settings_dict
                    )
                    rabbit_mq_string = "BROKER_URL = 'amqp://%s:%s@127.0.0.1:5672//%s'" % (PROJECT_NAME, PROJECT_NAME, PROJECT_NAME)
                    
                    run_func('echo -e "%s\n\n%s\n\n%s\n\n%s" > src/project/settings_local.py' % (debug_string, template_debug_string, settings_string, rabbit_mq_string))
        
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
                
                # create db stuff
                run_func('sudo -u postgres createuser -D -A -P %s' % PROJECT_NAME)
                run_func('sudo -u postgres createdb -O %s %s' % (PROJECT_NAME, PROJECT_NAME))
                
                # create rabbitmq stuff
                run_func('sudo rabbitmqctl add_user %s %s' % (PROJECT_NAME, PROJECT_NAME))
                run_func('sudo rabbitmqctl add_vhost /%s' % PROJECT_NAME)
                run_func('sudo rabbitmqctl set_permissions -p /%s %s ".*" ".*" ".*"' % (PROJECT_NAME, PROJECT_NAME))
                
    
            # restart supervisor processes
            run_func('sudo supervisorctl restart %s.gunicorn' % server_name)
            run_func('sudo supervisorctl restart %s.celeryd' % server_name)
            if nginx_conf_changed:
                with settings(warn_only=True):
                    if run_func("test -d crt/%s.crt" % server_name).failed:
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
        