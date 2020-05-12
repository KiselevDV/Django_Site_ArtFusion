sudo apt install python3-pip
sudo pip3 install virtualenv
virtualenv djangoenv
source djangoenv/bin/activate
in win case: djangoenv\Scripts\activate

pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

### https://django-ckeditor.readthedocs.io/en/latest/