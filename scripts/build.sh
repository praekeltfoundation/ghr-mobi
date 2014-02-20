#!/bin/bash

cp -a ghr-mobi/src ./build/ghr-mobi
mkdir -p ./build/ghr-mobi/media/uploads
touch ./build/ghr-mobi/media/uploads/Keep

${PIP} install -r ghr-mobi/requirements.txt

