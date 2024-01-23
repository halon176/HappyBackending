#!/bin/sh

celery --app=src.tasks.tasks:celery flower
