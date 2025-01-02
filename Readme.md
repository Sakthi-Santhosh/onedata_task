1. Clone the repository:
   https://github.com/Sakthi-Santhosh/onedata_task.git
   cd onedata_task

2.Install dependencies:

    pip install -r requirements.txt

3.Run migrations:

    change the db configuration if need to use mysql 

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'mydb',
            'USER': 'root',
            'PASSWORD': 'admin',
            'HOST':'localhost',
            'PORT':'3306',
        }
    }


    python manage.py migrate

4.Create a superuser:

    python manage.py createsuperuser

5.Start the server:

    python manage.py runserver

6.Check the API collection in one data.postman_collection.json within the project folder

7.Credentials:

    superuser:
        username:admin
        password:12345