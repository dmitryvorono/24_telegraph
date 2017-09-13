# Telegraph Clone

Telegraph Clone is a clone of [telegra.ph](http://telegra.ph/). Everyone can use this app for write and publish articles to Internet.

[Open app](https://ancient-basin-28805.herokuapp.com)

# How to install local

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
$ pip install -r requirements.txt # alternatively try pip3
```
Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.

Next, run app:

```bash
$ gunicorn server:app
```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
