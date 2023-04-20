"""Collect all tasks into the same file for easy management"""

from celery import shared_task
from .gist import createGist


createGist = shared_task(createGist)
