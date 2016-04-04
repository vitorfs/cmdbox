#!/bin/bash

flake8 cmdbox
coverage run --branch manage.py test --settings=cmdbox.tests_settings --verbosity=1
coverage html
