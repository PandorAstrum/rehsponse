# REHSPONSE
> A social web app

[![Python Version][python-image]][python-url]
[![Django Version][django-image]][django-url]

One to two paragraph statement about your product and what it does.

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
    └── template (folder)                   # default template folder

## Usage example

Settings is split into local and prod 

- To run the app into local environment

```
truffle compile
```

- To run the app into production:
```
truffle migrate
```


## Release History

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
