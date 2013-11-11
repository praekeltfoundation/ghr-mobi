from setuptools import setup, find_packages

setup(
    name='app',
    version='0.0.1',
    description='Website',
    author='Unomena Developers',
    author_email='dev@unomena.com',
    url='http://unomena.com',
    packages = find_packages('src'),
    package_dir = {'': 'src'},
    dependency_links = [
        'http://github.com/unomena/django-photologue/tarball/2.8.praekelt#egg=django-photologue-2.8.praekelt',
        'http://github.com/unomena/django-ckeditor-new/tarball/3.6.2.2#egg=django-ckeditor-3.6.2.2'
    ],
    install_requires = [
        'South',
	    'unipath',
        'django-countries',
        'django-debug-toolbar',
        'django-polymorphic',
        'django-ckeditor==3.6.2.2',
        'django-photologue==2.8.praekelt',
        'django-registration==1.0',
        'django-preferences',
        'python-memcached',
        'django_compressor',
        'gunicorn',
        'celery==3.0.23',
        'django-celery==3.0.23',
        'django-honeypot',
        'Pillow',
        'psycopg2',
        'flufl.password==1.2.1',
        'tunobase'
    ],
    include_package_data=True,
)
