import getpass

APP_NAME = 'app'

REPO_PATH = 'unomena/unomena-starter'

PROJECT_NAME = 'unomena-starter'

IN_HOUSE_DOMAIN = 'unomena.net'

FRONTEND_PROXY_PORT = '12000'

HTTPS_PORT = '443'

PRODUCTION_SERVER_NAME = 'unomena-starter.com'

DEPLOY_USER = getpass.getuser()

DEV_SERVERS = ['ubuntu@precise.dev.unomena.net']

QA_SERVERS = ['ubuntu@precise.qa.unomena.net']

PROD_SERVERS = ['ubuntu@web1.prod.unomena.net', 'ubuntu@web2.prod.unomena.net']