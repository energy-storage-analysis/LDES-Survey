
# Setup python environment

cd requirements
python -m pip install -r requirements.txt

# Run setup script, main purpose is setting up the es_utils package in the local environment.

cd ..
python setup.py install


# Install Seaborn Fork
# Some custom changes have been made to the seaborn plotting library and it is included as a git submodule of a fork on GitHub.

git submodule init
git submodule update

cd seaborn
python setup.py install