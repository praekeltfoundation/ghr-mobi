from setuptools import setup, find_packages

setup(
    name='unomena',
    version='0.0.1',
    description='Website',
    author='Unomena Developers',
    author_email='dev@unomena.com',
    url='http://unomena.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    dependency_links = [
        'http://github.com/unomena/django-photologue/tarball/2.7.praekelt#egg=django-photologue-2.7.praekelt',
        #'http://git.unomena.net/unomena/tunobase/repository/archive?ref=0.0.1.beta',
        #'http://git.unomena.net/unomena/unobase/repository/archive?ref=1.3.3.beta'
    ],
    install_requires = [
    	#'tunobase==0.0.1.beta',
        'fabric',
        'South',
	    'unipath',
        'django-countries',
        'django-debug-toolbar',
        'django-polymorphic',
        'django-ckeditor==3.6.2.1',
        'django-photologue==2.7.praekelt',
        'django-registration==1.0',
        'django-preferences',
        'python-memcached',
        'gunicorn',
        'celery==3.0.15',
        'django-celery==3.0.11',
        'django-honeypot',
        'Pillow',
        'psycopg2',
    ],
    include_package_data=True,
)
