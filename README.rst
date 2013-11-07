Alogator
============

Alogator is an aggregated logging actor system. PLEASE NOTE: This Django app is in α state! Don't use it yet - unless you're ready to falling down the rabbit hole. ;-) 


Installation
------------

To get the latest stable release from PyPi (not released yet!)

.. code-block:: bash

    pip install alogator

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/arteria/alogator.git#egg=alogator

TODO: Describe further installation steps (edit / remove the examples below):

Add ``alogator`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'alogator',
    )




Don't forget to create the tables for your database

.. code-block:: bash

    ./manage.py syncdb alogator


Usage
-----

Setup your logfiles, search patterns and actors in the admin backend.

To run one (scan all logfiles for patterns) just call the ``scanlogfiles`` management command.

.. code-block:: bash
	
	python manage.py scanlogfiles

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

Histroy
-------

Please refer to CHANGELOG.txt

Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 alogator
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
