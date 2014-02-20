#!/bin/bash

cp -a ghr-mobi/src ./build/ghr-mobi

mkdir -p ./build/ghr-mobi/project/media/uploads
mkdir -p ./build/ghr-mobi/project/whoosh
mkdir -p ./build/ghr-mobi/project/static

touch ./build/ghr-mobi/project/media/uploads/Keep
touch ./build/ghr-mobi/project/whoosh/Keep
touch ./build/ghr-mobi/project/static/Keep

${PIP} install -r ghr-mobi/requirements.txt

