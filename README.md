# Youtube Searcher
Django application for searching some videos on Youtube hosting by users keywords.

supported Python versions: 3.5, 3.6, 3.7

### How to install? ###
```bash
cd <path_to_project>
git clone git@github.com:DmitryBurnaev/youtube-keywords.git youtube_keywords
cd youtube_keywords
python3 -m venv venv
source venv/bin/activate
pip install -r requiriments.txt
cd src
cp conf/settings_local.py.template conf/settings_local.py
nano conf/settings_local.py  #  change something if it is needed
```

### How to setup and run? ###
```bash
cd <PATH_TO_PROJECT>
source venv/bin/activate

cd src
export PYTHONPATH=$(pwd):${PYTHONPATH}
export YOUTUBE_API_KEY=<YOUR_API_KEY>

# optional
export CELERY_BROKER_URL=redis://docker.redis:6379/1

# migrate db
python manage.py migrate

# create new superuser
python manage.py createsuperuser

# run server in develop mode
python manage.py runserver

```

#### YOUTUBE_API_KEY

You can click on this link: https://developers.google.com/youtube/v3/getting-started
and get needed manual for creation API key.



### Simple way: run and install via Docker-compose

```bash

cd <PATH_TO_PROJECT>
echo "YOUTUBE_API_KEY=<YOUR_API_KEY>" > .env
docker-compose build
docker-compose up -d

# create superuser
docker-compose exec web python manage.py createsuperuser
```