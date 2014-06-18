manage="${VENV}/bin/python ${INSTALLDIR}/ghr-mobi/manage.py"
pip="${VENV}/bin/pip"

$pip install http://github.com/unomena/django-ckeditor-new/tarball/3.6.2.2#egg=django-ckeditor-3.6.2.2
$pip install http://github.com/unomena/django-photologue/tarball/2.8.praekelt#egg=django-photologue-2.8.praekelt
$pip install http://github.com/unomena/tunobase/tarball/1.0.10#egg=tunobase-1.0.10
$pip install http://github.com/unomena/django-holodeck/tarball/0.1.2#egg=django-holodeck-0.1.2
$pip install http://github.com/unomena/photon/tarball/0.0.6#egg=photon-0.0.6

$manage syncdb --noinput --no-initial-data --migrate
$manage collectstatic --noinput
