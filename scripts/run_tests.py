#!/bin/bash

flake8 cmdbox
coverage run --branch manage.py test --settings=cmdbox.tests_settings --verbosity=2
coverage html
