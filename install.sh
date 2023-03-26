cd requirements
python -m pip install -r requirements.txt
cd ..
python setup.py install

git submodule init
git submodule update

cd seaborn
python setup.py install