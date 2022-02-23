

### Getting Started

Install dependencies with:```pip install -r requirements.txt```

Assuming a configured postgresql database for local development user,
run the initial migration with:

```python manage.py migrate```

so that you get something with
```./manage.py runserver```

Enjoy and pull requests welcome.

### Additional

For live reload,

```pip install django-livereload-server``` where there will be separate watch process [as per here](https://github.com/tjwalch/django-livereload-server)

Enjoy live reloading!
