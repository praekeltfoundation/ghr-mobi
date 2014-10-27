manage="${VENV}/bin/python ${INSTALLDIR}/ghr-mobi/manage.py"
pip="${VENV}/bin/pip"

$pip install http://github.com/unomena/django-ckeditor-new/tarball/3.6.2.2#egg=django-ckeditor-3.6.2.2
$pip install http://github.com/unomena/django-photologue/tarball/2.8.praekelt#egg=django-photologue-2.8.praekelt
$pip install http://github.com/unomena/tunobase/tarball/1.0.10#egg=tunobase-1.0.10
$pip install http://github.com/smn/django-holodeck/tarball/0.1.5#egg=django-holodeck-0.1.5
$pip install http://github.com/unomena/photon/tarball/0.0.6#egg=photon-0.0.6

DJANGO_SETTINGS_MODULE="project.settings" $manage syncdb --noinput --no-initial-data --migrate
DJANGO_SETTINGS_MODULE="project.settings" $manage collectstatic --noinput
