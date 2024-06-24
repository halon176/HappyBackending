#!/bin/sh

celery --app=src.tasks.tasks:celery worker -l INFO

