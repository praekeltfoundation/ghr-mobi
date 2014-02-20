manage="${VENV}/bin/python ${INSTALLDIR}/ghr-mobi/manage.py"

$PIP install http://github.com/unomena/django-ckeditor-new/tarball/3.6.2.2#egg=django-ckeditor-3.6.2.2
$PIP install http://github.com/unomena/django-photologue/tarball/2.8.praekelt#egg=django-photologue-2.8.praekelt
$PIP install http://github.com/unomena/tunobase/tarball/1.0.9#egg=tunobase-1.0.9

$manage syncdb --noinput --no-initial-data --migrate
$manage collectstatic --noinput
