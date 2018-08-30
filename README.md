# Youtube Searcher
Django application for searching some videos on Youtube hosting by users keywords.

### How to install? ###
```bash
cd <path_to_project>
git clone git@github.com:DmitryBurnaev/youtube-keywords.git youtube_keywords
cd youtube_keywords
python3 -m venv venv
pip install -r requiriments.txt
cp conf/settings_local.py.template conf/settings_local.py
nano conf/settings_local.py  #  change something if it is needed
```

### How to setup and run? ###
```bash
cd <path_to_project>
source venv/bin/activate

cd src
export PYTHONPATH=$(pwd)
export YOUTUBE_API_KEY=<your-api-key-from-googleapi>

# run server in develop mode
python manage.py runserver

```

#### YOUTUBE_API_KEY

You can click on this link: https://developers.google.com/youtube/v3/getting-started
and get needed manual for creation API key.

