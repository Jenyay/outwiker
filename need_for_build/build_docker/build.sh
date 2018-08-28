#!/bin/sh
pipenv update --dev && pipenv run fab "$@"
