# Department of Treat Vending Website

## Create Database Tables
```bash
poetry shell
python manage.py makemigrations branch_services # set up the migration that creates the database stuff
python manage.py check # make sure we aren't going to screw this up
python manage.py migrate # create the database
python manage.py createsuperuser # get an admin panel
```

## Quick Run
```bash
poetry shell
python manage.py runserver
```

Go to [localhost:8000](localhost:8000) to see the webpage!

## Apps
### [Branch Services](http://localhost:8000/branch_services/)

## Getting Started
[Good Django tutorial](https://docs.djangoproject.com/en/4.1/intro/tutorial01/)