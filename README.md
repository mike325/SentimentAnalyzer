# Welcome to the open sentiment analyzer API !

[![Travis Status](https://travis-ci.com/Mike325/SentimentAnalyzer.svg?token=3YWhs8nPpqyajna6si5D&branch=master)](https://travis-ci.com/Mike325/SentimentAnalyzer)
[![Github Status](https://github.com/Mike325/SentimentAnalyzer/workflows/analyzer/badge.svg)](https://github.com/Mike325/SentimentAnalyzer/actions)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)


This project attempts to create an open API to allow developers to analyze
topics/searches from social networks and extract the average sentiment.

ToDo list

- [ ] Document the API and the project
- [X] Enable at least one social network API (Twitter)
- [X] Enable crawler script which uses social networks APIs
- [X] Enable historic and real time queries
- [X] Create simple access point for topic analyze
- [ ] Create pluggable analyzers
  - [X] Enable dummy random analyzer
  - [ ] Enable real sentiment analyzer
- [ ] Add and authentication method (user-password/token or other method)
- [ ] Stabilize API
- [ ] Use test cases to cover API functionality

## REST API

To run the project locally first be sure to have a
[twitter API](https://developer.twitter.com/en/apply-for-access) onces you have access install [python>=3.6](https://www.python.org/downloads/) and all development dependencies with

```sh
$ # Virtual environments are the recommended way to test this project
$ virtualenv -p python3 ./env && source ./env/bin/activate # or ./env/Scripts/activate for Windows
(env)$ pip3 install -r requirements/requirements.txt
(env)$ python manage.py migrate # create the database
```
Currently the system only supports twitter's API,
you could set the tokens with environment variables as:

```sh
$ export TWITTER_TOKEN_KEY="API_KEY"
$ export TWITTER_TOKEN_SECRET"API_SECRET"
```

Or with a json file in the `./server/apps/crawler/social/settings.json` with the following format

```json
{
    "twitter": {
        "token": {
            "key": "API_KEY",
            "secret": "API_SECRET"
        }
    }
}
```

Once the API tokens are created, you could test the system with:

```sh
(env)$ # if you want to run the tests, install the dev dependencies
(env)$ pip3 install -r requirements/dev.txt # dev_windows.txt for Windows
(env)$ bash -C 'test/test.sh'
```

Note: The environment variable will be preferred than the json file.


Finally to test the API run `python3 manage.py runserver` and the local server
should be available at `localhost:8000`, the admin is in /admin/ and the API
entry point is in /api/

## Crawler

The system also supports "standalone" use of the crawler, so far the crawler
needs Django's the database capabilities that's the reason it's not fully
independent script, to use the crawler script to pull social network data
(Twitter at this point) use the following commands

```sh
$ # Virtual environments are the recommended way to test this project
$ virtualenv -p python3 ./env && source ./env/bin/activate # or ./env/Scripts/activate for Windows
(env)$ pip3 install -r requirements/requirements.txt # if they are not installed yet
(env)$ python manage.py migrate # If the database hasn't been created
(env)$ python ./server/apps/crawler/apps.py --help # To get all available options
(env)$ python ./server/apps/crawler/apps.py --query "#foo" --trend Mexico --network twitter
```

## FAQ

### Cool, How could I get data from the API?
**A:** After the project is running you could get data from the available
analyzers doing a POST request to /api/topic/<TOPIC_ID>/analyze


The POST request must be a json with the following data
```json
{
  "method": "<ANALYZER_NAME>",
  "date": {
    "start": "YYYY/MM/DD",
    "end": "YYYY/MM/DD"
  }
}
```
Only one of the "start/end" keys is required, which means to analyze from one
date up to today or analyze every date from the dawn to the "end" date
(inclusive), if both are give, then only the time frame between start and end
(inclusive) will be analyze.


**NOTE**: Please take into consideration

### How can I add new analyzers?
**A:** The system is dynamic, so add new analyzers it's quite simple,
all modules inside `server/nlp/` with a py file named `analyzer` with method named
`analyze`  with will be candidates to be used by de API, the `analyze` method
must receive and argument of type `django.db.model.Model` and must return a
dictionary with the results take a look at `server/nlp/random` to get a glance
of how it should be structured.

### When the project will be ready to test it out?
**A:** The project is in a very early stage (pre-alpha at best), even tho
there's no date for a "official" release I hope the API is stabilized this year
so anyone could use the project without any breaking changes every commit.
