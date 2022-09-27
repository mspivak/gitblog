# Gitblog
A minimalist git+markdown blogging platform.

## Develop

To start Django's local webserver
```bash
$ python manage.py runserver --settings=gitblog.settings_dev
```

To start Tailwind CSS compiler + reloader
```bash
$ python manage.py tailwind start
```



## Deploy

```bash
$ python manage.py tailwind build
$ serverless deploy
```