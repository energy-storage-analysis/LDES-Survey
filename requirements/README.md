This folder contains various ways to create a python environment to run the codes in the repository. 

`requirements.txt`: The requirements file used to test the final figures in the manuscript
`requirements_full.txt`: The export of the created final environment, including specific designation of dependencies determined by pip at the time of the install.
`environment.yml`: The conda environment used throughout development of the repository, but not the final figures. Created with `conda env export`
`environment_from_history.yml`: The same as `environment.yml` but created with the `--from-history` flag. Might work better on linux. 