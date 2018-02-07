#!/bin/bash

python googlesearch/setup.py install

echo -e "\nmusify(){
	python $PWD/musify.py \"\$1\"
}" >> ~/.zshrc
