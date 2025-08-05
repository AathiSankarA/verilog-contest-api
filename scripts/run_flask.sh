# activate virtual environment
source ./env/bin/activate 

# install requirements
if [ "$1" == "d" ]; 
then 
flask run --debug --host 0.0.0.0 
else 
flask run --host 0.0.0.0 
fi

# deactivate environment
deactivate
