# wellboreStore_Oreb

## clone repo
git clone https://gitlab.com/conradsuuna.cs/wellborestore_oreb.git

## add .env file
touch .env

copy contents from .ENVEXAMPLE and paste them in .env

## create a virtual environment
python -m venv chosen_name

## activate virtual environment
source chosen_name/bin/activate

## install dependencies 
python -m pip install -r requirements.txt

## create database in Azure data studio
CREATE DATABASE WellBoreStoreDB;
GO

# For local usage (models)
### flask db init
Creates a new migration repository.

### flask db migrate
Autogenerate a new revision file (Alias for 'revision...

### flask db upgrade
Then you can apply the migration to the database (Upgrade to a later version)
<!-- flask db stamp head -->

## run project
flask run
or
python app.py
