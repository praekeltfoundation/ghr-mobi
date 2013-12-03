import getpass

APP_NAME = 'app'

REPO_PATH = 'praekelt/ghr'

PROJECT_NAME = 'ghr'

IN_HOUSE_DOMAIN = 'unomena.net'

FRONTEND_PROXY_PORT = '12005'

HTTPS_PORT = '443'

PRODUCTION_SERVER_NAME = 'girlhub-rwanda.com'

DEPLOY_USER = getpass.getuser()

USE_CELERY = True

DEV_SERVERS = ['ubuntu@precise.dev.unomena.net']

QA_SERVERS = ['ubuntu@precise.qa.unomena.net']

PROD_SERVERS = ['ubuntu@web1.prod.unomena.net', 'ubuntu@web2.prod.unomena.net']

TESTS_TO_RUN = (
    'tunobase.core '
    'tunobase.blog '
    'tunobase.commenting '
    'tunobase.poll '
    'tunobase.social_media.tunosocial'
)