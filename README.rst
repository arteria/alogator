Alogator
============

Alogator is an aggregated logging actor system. PLEASE NOTE: This Django app is in α state! Don't use it yet - unless you're ready to falling down the rabbit hole. ;-) 


.. contents:: Table of Contents


Installation
------------

To get the latest stable release from PyPi (not released yet!)

.. code-block:: bash

    pip install alogator

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/arteria/alogator.git#egg=alogator

TODO: Describe further installation steps (edit / remove the examples below):

Add ``alogator`` to your ``INSTALLED_APPS`` and define a logger

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'alogator',
    )

    LOGFILE_PATH = os.path.join(os.path.join(BASE_DIR, 'logs/'), "alogator.log")

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'formatters': {
            'standard': {
                'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
                'datefmt': "%d/%b/%Y %H:%M:%S"
            },
        },
        'handlers': {
            'logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOGFILE_PATH,
                'maxBytes': 1000000,
                'backupCount': 0,
                'formatter': 'standard',
            }
        },
        'loggers': {
            'alogator': {
                'handlers': ['logfile'],
                'level': 'DEBUG',
            },
        }
    }




Don't forget to create the tables for your database

.. code-block:: bash

    ./manage.py syncdb alogator
    # python manage.py migrate


Usage
-----

Setup your logfiles, search patterns and actors in the admin backend.

To run one (scan all logfiles for patterns) just call the ``scanlogfiles`` management command.

.. code-block:: bash
    
    python manage.py scanlogfiles

You can use ``alogator_cli`` to check the log files in a project. Simple add paths to settings files as arguments. Be aware that you have to run the project, so you need to first activate your virtualenv if you have one.

.. code-block:: bash

    # if you have a virtualenv
    . /path/to/env/bin/activate

    alogator_cli /path/to/project/settings.py

To run this continously you could setup a cronjob. For example, to run this every other minute use

.. code-block:: bash

    crontab -e
    
Than add 

.. code-block:: bash

    */2 * * * * /path/to/your/manage.py scanlogfiles
    
You may have to activate your virtualenv depending on your setup.



TODO
----

* Customizable temporary working dir instead of /tmp
* Customizable subject, eg. [Alogator] (to filter inbox)
* Add "To mute this actor, visit..." in message/email.

Histroy
-------

Please refer to CHANGELOG.txt


Contribute
----------

If you want to contribute to this project, simply send us a pull request. Thanks. :)
