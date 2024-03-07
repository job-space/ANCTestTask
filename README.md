
## About
 
Instructions for installing the project

download the project locally 
 - git clone https://github.com/job-space/ANCTestTask.git
create a virtual environment 
 - python -m venv venv 
 - .\venv\Scripts\activate 
upload requirements.txt
 - pip install -r requirements.txt 
make database migrations 
 - python manage.py makemigrations
 - python manage.py migrate 
upload test data 
 - python seed_data.py
run the project
 - python manage.py runserver
 
 ## Developers
 
[y.kovalchuk](https://github.com/job-space)

## License

Project YourLibraryProposes is distributed under the MIT lisense.
