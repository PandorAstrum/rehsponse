# REHSPONSE
> A social web app with a REST API

[![Python Version][python-image]][python-url]
[![Django Version][django-image]][django-url]



![header-pic]

## Requirement (Windows | MAC | LINUX)
- [x] [Python](https://www.python.org/)
- [x] [Django](https://www.djangoproject.com/)
- [x] [git cli](https://git-scm.com/downloads)
- [x] [Pipenv]() ``Not required but recommended``


## Installation & Setup

OS X & Linux & Windows:

open command prompt or terminal 

* Go to the directory where you want to download :

```bash
git clone https://github.com/PandorAstrum/rehsponse.git
```
* install pipenv or virtualenv via pip:
```bash
pip install pipenv
```
* create a virtual environment and install all dependency from ```Pipfile```:
```bash
pipenv install
```

## Folder Structure
*project root*

    ├── src (folder)                        # contains django backbone
    ├── rehsponse (folder)                  # contains the app
    |   └── api (folder)                    # contains the api
    ├── static-serve (folder)               # serving css js and image
    ├── static-storage (folder)             # storing img
    └── template (folder)                   # default template folder

## Usage example

Settings is split into dev and prod 

- To run the app into local environment

```
python manage.py runserver DJANGO_SETTINGS_MODULE=settings.dev
```

- To run the app into production:
```
python manage.py runserver DJANGO_SETTINGS_MODULE=settings.prod
```

## API overview

- Authorization token or Login (POST)

```
/api/login/
```

~ equivalent in django app ``None``

- Rehsponse Get All (GET)

```
/api/list/
```
 ~ equivalent in django app ``/`` or ``home/``

- Create a Rehsponse or reply to a rehsponse (POST)

```
/api/rehsponse/create/
```
 ~ equivalent in django app ``/rehsponse/create``

- A single Rehsponse (GET)

```
/api/rehsponse/<id>/
```
 ~ equivalent in django app ``/rehsponse/1``
 
- Edit a rehsponse (PUT, PATCH)

```
/api/rehsponse/<id>/edit/
```
 ~ equivalent in django app ``/rehsponse/1/edit``

- Delete a rehsponse (POST)

```
/api/rehsponse/<id>/delete/
```
 ~ equivalent in django app ``/rehsponse/1/delete``
 
- Love a Rehsponse

```
/api/rehsponse/<id>/loved/
```

~ equivalent in django app ``None``


- Get all tags and show (GET)

```
/api/tags/
```

~ equivalent in django app ``/tags/``

- Get contacts (GET)

```
/api/contacts/
```

~ equivalent in django app ``/contacts/``

- Get single User and associated account (GET)

```
/api/user/<str:username>/rehsponses
```

~ equivalent in django app ``/user/1234567890/rehsponse``

- Create a user or register (Post)

```
/api/user/create
```

~ equivalent in django app ``/user/create``

- Edit a user profile (PUT, PATCH)

```
/api/user/<str:username>/edit
```

~ equivalent in django app ``/user/1234567890/edit``

- Delete a user (POST)

```
/api/user/<str:username>/delete
```

~ equivalent in django app ``/user/1234567890/delete``

## Work History
* 0.2.5
    * FIXED: Only edit button reveals to post owner
* 0.2.4
    * ADD: RESPOND to a response
* 0.2.3
    * ADD: Love feature on response
* 0.2.2
    * ADD: Dynamic contact page and navigations
* 0.2.1
    * ADD: SITEMAP for SEO
* 0.2.0
    * ADD: User token authentication
    * CHANGE: All call to endpoints now require authentication
* 0.1.9
    * ADD: auto username generation on profile create
    * CHANGE: first name query to username for all user model
* 0.1.8
    * FIXED: hashtag auto creation and marking with user profile
* 0.1.7
    * ADD: hash tag api and jquery
* 0.1.6
    * ADD: Asynchronous pagination and load more 
* 0.1.5
    * ADD: Search Query and filters
* 0.1.4
    * ADD: AJAX call to endpoints in html
* 0.1.3
    * ADD: Views in django app for all routes (jQUERY)
* 0.1.2
    * ADD: user api (LIST/RETRIEVE/UPDATE/DELETE)
* 0.1.1
    * ADD: rehsponse api (LIST/RETRIEVE/UPDATE/DELETE)
* 0.1.0
    * ADD: forms and modals template
* 0.0.9
    * CHANGE: template merge with api
* 0.0.8
    * ADD: Add api folder and django rest routes
* 0.0.7
    * ADD: app model and views with route
* 0.0.6
    * ADD: all template
* 0.0.5
    * ADD: docker, flake8 and travis CI
* 0.0.4
    * ADD: Add git ignore, readme and licence
* 0.0.3
    * FIX: project renamed into ``src``
* 0.0.2
    * CHANGED: Settings Split For Digital Ocean deployment
* 0.0.1
    * Work in progress

## Meta

Ashiquzzaman Khan – [@dreadlordn](https://twitter.com/dreadlordn)

Distributed under the GPL license. See ``LICENSE`` for more information.

[https://github.com/PandorAstrum/rehsponse.git](https://github.com/PandorAstrum/rehsponse.git)

## Contributing

1. Fork it (<https://github.com/PandorAstrum/rehsponse.git>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's -->
[python-image]: https://img.shields.io/badge/Python-3.6-yellowgreen.svg?style=flat-square&logo=python
[python-url]: https://www.python.org/

[django-image]: https://img.shields.io/badge/Django-3.0-orange.svg?style=flat-square&logo=django
[django-url]: https://www.djangoproject.com/
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square

[travis-image]: https://travis-ci.org/PandorAstrum/_vault.svg?branch=master
[travis-url]: https://travis-ci.org/PandorAstrum/_vault

[appveyor-image]: https://ci.appveyor.com/api/projects/status/8dxrtild5jew79pq?svg=true
[appveyor-url]: https://ci.appveyor.com/project/PandorAstrum/vault

[ReadTheDoc]: https://github.com/yourname/yourproject/wiki

<!-- Header Pictures and Other media-->
[header-pic]: Readme_Template/header.png
