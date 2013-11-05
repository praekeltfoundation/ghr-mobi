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

def _run_as_pg(command):
    """
    Run command as 'postgres' user
    """
    with cd('~postgres'):
        return run('sudo -u postgres %s' % command)
    
def pg_user_exists(name):
    """
    Check if a PostgreSQL user exists.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'), warn_only=True):
        res = _run_as_pg('''psql -t -A -c "SELECT COUNT(*) FROM pg_user WHERE usename = '%(name)s';"''' % locals())
    return (res == "1")

def pg_database_exists(name):
    """
    Check if a PostgreSQL database exists.
    """
    with settings(hide('running', 'stdout', 'stderr', 'warnings'),
                  warn_only=True):
        return _run_as_pg('''psql -d %(name)s -c ""''' % locals()).succeeded

def _email_project_deployed(instance_type):
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
    
def _get_local_settings(instance_type):
    settings_list = []
    settings_dict = {
        'engine': 'django.db.backends.postgresql_psycopg2',
        'name': instance_type in ['dev', 'qa'] and '%s_%s' \
            % (PROJECT_NAME, instance_type) or PROJECT_NAME,
        'user': PROJECT_NAME,
        'password': PROJECT_NAME,
        'host': 'localhost',
        'port': '5432'        
    }
    
    settings_list.append('DEBUG = %s' % 'False' if instance_type == 'master' else 'True')
    settings_list.append('TEMPLATE_DEBUG = DEBUG')
    settings_list.append(
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
    settings_list.append("BROKER_URL = 'amqp://%s:%s@127.0.0.1:5672//%s'" % (PROJECT_NAME, PROJECT_NAME, PROJECT_NAME))
    
    return '\n\n'.join(settings_list)

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
        run_func(
            'python bootstrap.py && '
            'bin/buildout buildout:server-names="%(server_name)s" '
            'buildout:server-name="%(server_name)s" '
            'buildout:app-name="%(app_name)s" '
            'buildout:frontend-proxy-port="%(frontend_proxy_port)s" '
            'buildout:https-port="%(https_port)s"'
            % buildout_config
        )
        
        if where == 'remote':
            # chowns
            run_func(
                'sudo chown -R ubuntu:unoweb bin && '
                'sudo chown ubuntu:unoweb logs && ' 
                'sudo chown ubuntu:unoweb scheduler && '
                'sudo chown ubuntu:unoweb static && '
                'sudo chown ubuntu:unoweb media'
            )
            
            # chmods
            run_func('sudo chmod -R 2775 bin && '
                'sudo chmod -R 2775 logs && '
                'sudo chmod 660 .installed.cfg && '
                'sudo chmod 2775 scheduler &&'
                'sudo chmod -R 2755 static &&'
                'sudo chmod 2775 media &&'
            )
            
            # mkdirs
            with settings(warn_only=True):
                if run_func("test -d media/uploads").failed:
                    run_func('mkdir media/uploads')
                    
                if run_func("test -d src/project/settings_local.py").failed:
                    run_func(
                        'touch src/project/settings_local.py && '
                        'echo -e "%s" > src/project/settings_local.py' % _get_local_settings()
                    )
        
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
                if not pg_user_exists(PROJECT_NAME):
                    _run_as_pg('createuser -D -A -P %s' % PROJECT_NAME)
                if not pg_database_exists(PROJECT_NAME):
                    _run_as_pg('createdb -O %s %s' % (PROJECT_NAME, PROJECT_NAME))
                
                # create rabbitmq stuff
                run_func(
                    'sudo rabbitmqctl add_user %s %s' % (PROJECT_NAME, PROJECT_NAME) + ' && '
                    'sudo rabbitmqctl add_vhost /%s' % PROJECT_NAME + ' && '
                    'sudo rabbitmqctl set_permissions -p /%s %s ".*" ".*" ".*"' % (PROJECT_NAME, PROJECT_NAME)
                )
    
            # restart supervisor processes
            run_func('sudo supervisorctl restart %s.gunicorn' % server_name)
            run_func('sudo supervisorctl restart %s.celeryd' % server_name)
            if nginx_conf_changed:
                run_func('bin/make_cert.sh')
                run_func('sudo service nginx restart')
                
        # restart rabbit
        run_func('sudo service rabbitmq-server restart')
        
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
    
    _email_project_deployed(instance_type)

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
        