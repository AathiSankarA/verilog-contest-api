# virtual environment
python3 -m venv env 

# activate virtual environment
source ./env/bin/activate 

# install requirements
pip install -r requirements.txt

# create database 
python3 -c 'from Application.application import create_app,db;from Application.controller import CAuth;app = create_app();db.create_all();CAuth.create_user("Admin" , "Admin-User")' 

# deactivate environment
deactivate 