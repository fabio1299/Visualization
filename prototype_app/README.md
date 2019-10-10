# Project Title
## Project Description Here

## Project Environment

This project uses the Anaconda package manager with the conda-forge channel. The package info is located in `requirements.txt`.

`conda create --name myenv --file  requirements.txt`

## Settings

Sensitive settings are stored in environment variables. One easy approach to working this way is store the variables 
in your conda activation scripts

```
# /~anaconda3/envs/myenv/etc/conda/activate.d/env_vars.sh
#Django Settings
export SECRET_KEY="super_secret"
export DEBUG="True"
export ALLOWED_HOSTS="10.16.67.12,10.56.43.23"

##Databases
export DB_HOST="10.16.67.02"
export DB_PORT="5432"
export DB_USER="username"
export DB_PASSWORD="password"
```

```
# /~anaconda3/envs/myenv/etc/conda/deactivate.d/env_vars.sh
unset SECRET_KEY
unset DEBUG
unset ALLOWED_HOSTS
unset DB_HOST
unset DB_PORT
unset DB_USER
unset DB_PASSWORD

```

