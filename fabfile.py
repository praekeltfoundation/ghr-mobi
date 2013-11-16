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

env.buildout_config = {
    'project_name': PROJECT_NAME,
    'frontend_proxy_port': FRONTEND_PROXY_PORT,
    'https_port': HTTPS_PORT,
    'app_name': APP_NAME
}

env.run_cmd = local

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
    
    settings_list.append('DEBUG = %s' % ('False' if instance_type == 'master' else 'True'))
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

def _get_server_name(instance_type):
    if instance_type == 'master':
        return PRODUCTION_SERVER_NAME
    
    return '%s.%s.%s' % (PROJECT_NAME, instance_type, IN_HOUSE_DOMAIN)

def _get_instanced_project_name(instance_type):
    if instance_type == 'master':
        return PROJECT_NAME
    
    return '%s_%s' % (PROJECT_NAME, instance_type)

def _run_as_pg(command):
    """
    Run command as 'postgres' user
    """
    return env.run_cmd('sudo -u postgres %s' % command)
    
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

def restart_supervisor(server_name):
    env.run_cmd('sudo supervisorctl restart %s.gunicorn' % server_name)
    if USE_CELERY:
        env.run_cmd('sudo supervisorctl restart %s.celeryd' % server_name)
        
def setup_rabbitmq(instanced_project_name):
    with settings(warn_only=True):
        env.run_cmd(
            'sudo rabbitmqctl add_user %s %s' % (instanced_project_name, instanced_project_name) + ' && '
            'sudo rabbitmqctl add_vhost /%s' % instanced_project_name + ' && '
            'sudo rabbitmqctl set_permissions -p /%s %s ".*" ".*" ".*"' % (instanced_project_name, instanced_project_name) + ' && '
            'sudo service rabbitmq-server restart'
        )
    
def symlink_nginx(server_name):
    with settings(warn_only=True):
        env.run_cmd('sudo rm /etc/nginx/sites-available/%s' % server_name)
        env.run_cmd('sudo ln -s $PWD/nginx/%s.conf /etc/nginx/sites-available/%s.conf' % (server_name, server_name))
        env.run_cmd('sudo rm /etc/nginx/sites-enabled/%s' % server_name)
        env.run_cmd('sudo ln -s $PWD/nginx/%s.conf /etc/nginx/sites-enabled/%s.conf' % (server_name, server_name))
        
def symlink_supervisor_gunicorn(server_name):
    with settings(warn_only=True):
        env.run_cmd('sudo rm /etc/supervisor/conf.d/%s.gunicorn.conf' % server_name)
        env.run_cmd('sudo ln -s $PWD/supervisor/gunicorn.conf /etc/supervisor/conf.d/%s.gunicorn.conf' % server_name)
        
def symlink_supervisor_celeryd(server_name):
    with settings(warn_only=True):
        env.run_cmd('sudo rm /etc/supervisor/conf.d/%s.celeryd.conf' % server_name)
        env.run_cmd('sudo ln -s $PWD/supervisor/celeryd.conf /etc/supervisor/conf.d/%s.celeryd.conf' % server_name)
        
def setup_postgres_database(instanced_project_name):
    with settings(warn_only=True):
        if not pg_user_exists(PROJECT_NAME):
            _run_as_pg('createuser -D -A -P %s' % PROJECT_NAME)
        if not pg_database_exists(instanced_project_name):
            _run_as_pg('createdb -O %s %s' % (PROJECT_NAME, instanced_project_name))
            
def setup_unoweb_group():
    with settings(warn_only=True):
        env.run_cmd(
            'sudo groupadd unoweb && '
            'sudo adduser ubuntu unoweb && ' 
            'sudo adduser www-data unoweb'
        )
        
def set_folder_permissions():
    # chowns
    env.run_cmd(
        'sudo chown -R ubuntu:unoweb bin && '
        'sudo chown ubuntu:unoweb logs && ' 
        'sudo chown ubuntu:unoweb scheduler && '
        'sudo chown ubuntu:unoweb static && '
        'sudo chown -R ubuntu:unoweb media'
    )
    
    # chmods
    env.run_cmd('sudo chmod -R 2775 bin && '
        'sudo chmod -R 2775 logs && '
        'sudo chmod 660 .installed.cfg && '
        'sudo chmod 2775 scheduler &&'
        'sudo chmod -R 2755 static &&'
        'sudo chmod -R 2775 media'
    )
    
def create_settings_local_file(instance_type):
    with settings(warn_only=True):   
        if env.run_cmd("test -d src/project/settings_local.py").failed:
            env.run_cmd('touch src/project/settings_local.py')
            env.run_cmd(
                'echo "%s" > src/project/settings_local.py' % _get_local_settings(instance_type)
            )

def build(where='local', first_deploy=False, instance_type='dev', 
                  nginx_conf_changed=False, code_dir='.'):
    assert where in ['local', 'remote'], "invalid option to where"
    
    if where == 'local':
        env.run_cmd = local
    elif where == 'remote':
        env.run_cmd = run
    
    server_name = _get_server_name(instance_type)
    instanced_project_name = _get_instanced_project_name(instance_type)
        
    env.buildout_config.update({
        'server_name': server_name
    })
    
    with cd(code_dir):
        env.run_cmd('python bootstrap.py')
        env.run_cmd(
            'bin/buildout buildout:server-names="%(server_name)s" '
            'buildout:server-name="%(server_name)s" '
            'buildout:app-name="%(app_name)s" '
            'buildout:frontend-proxy-port="%(frontend_proxy_port)s" '
            'buildout:https-port="%(https_port)s"'
            % env.buildout_config
        )
        
        if where == 'remote':
            if nginx_conf_changed:
                # symlink nginx
                symlink_nginx(server_name)
                
            if first_deploy:
                # setup unoweb group
                setup_unoweb_group()
                
                # set folder permissions
                set_folder_permissions()
                
                # create settings_local file
                create_settings_local_file(instance_type)
                
                # symlink supervisor gunicorn
                symlink_supervisor_gunicorn(server_name)
                
                # symlink supervisor celeryd if in settings
                if USE_CELERY:
                    symlink_supervisor_celeryd(server_name)
                
                # create db stuff
                setup_postgres_database(instanced_project_name)
                    
                # setup rabbitmq stuff
                setup_rabbitmq(instanced_project_name)
                
                # reload supervisor config
                env.run_cmd('sudo supervisorctl reload')
                
                # make cert file
                env.run_cmd('bin/make_cert.sh')
            else:
                # restart supervisor processes
                restart_supervisor(server_name)
                
            if nginx_conf_changed:
                # restart nginx
                env.run_cmd('sudo service nginx restart')
        
        # restart memcached
        env.run_cmd('sudo service memcached restart')
        
        # sync db
        env.run_cmd('bin/django syncdb')
        
        # run migrations
        env.run_cmd('bin/django migrate')
        
def prep():
    with settings(warn_only=True):
        local('git add . && git commit')
        local('git push')
    
def test_repo_exists(code_dir):
    with settings(warn_only=True):
        if env.run_cmd("test -d %s" % code_dir).failed:
            env.run_cmd("git clone git@git.unomena.net:%s.git %s" % (REPO_PATH, code_dir))

def deploy(first_deploy, instance_type, code_dir):
    env.run_cmd('git checkout %s' % instance_type)
    env.run_cmd('git pull origin %s' % instance_type)
    
    # todo: git diff code to determine if nginx conf changed
    # git diff HEAD:full/path/to/foo full/path/to/bar
    
    build('remote', first_deploy, instance_type, True, code_dir)
    
    _email_project_deployed(instance_type)
    
def pull(code_dir, instance_type, push_first=False):
    if push_first:
        prep()
    
    with cd(code_dir):
        env.run_cmd('git pull origin %s' % instance_type)

@roles('dev_server')
def deploy_dev(first_deploy=False):
    code_dir = '/home/ubuntu/dev/%s' % PROJECT_NAME
    instance_type = 'dev'
    
    test_repo_exists(code_dir)
    
    with cd(code_dir):
        deploy(first_deploy, instance_type, code_dir)
        
@roles('qa_server')
def deploy_qa(first_deploy=False):
    code_dir = '/home/ubuntu/qa/%s' % PROJECT_NAME
    instance_type = 'qa'
    
    test_repo_exists(code_dir)
    
    with cd(code_dir):
        deploy(first_deploy, instance_type, code_dir)
        
@roles('prod_servers')
def deploy_prod(first_deploy=False):
    code_dir = '/var/www/%s' % PROJECT_NAME
    instance_type = 'master'
    
    test_repo_exists(code_dir)
    
    with cd(code_dir):
        deploy(first_deploy, instance_type, code_dir)
        
@roles('dev_server')
def pull_dev(push_first=False):
    code_dir = '/home/ubuntu/dev/%s' % PROJECT_NAME
    pull(code_dir, 'dev', push_first)
    
@roles('qa_server')
def pull_qa(push_first=False):
    code_dir = '/home/ubuntu/qa/%s' % PROJECT_NAME
    pull(code_dir, 'qa', push_first)
    
@roles('prod_servers')
def pull_prod(push_first=False):
    code_dir = '/var/www/%s' % PROJECT_NAME
    pull(code_dir, 'master', push_first)
        
@roles('dev_server')
def restart_dev():
    restart_supervisor(_get_server_name('dev'))

@roles('qa_server')
def restart_qa():
    restart_supervisor(_get_server_name('dev'))
    
@roles('prod_servers')
def restart_prod():
    restart_supervisor(_get_server_name('dev'))