"""
docs/views.py
"""
import os

from django.conf import settings
from django.contrib.staticfiles.views import serve
from django.http import Http404


def api_docs(request, path):
    # user = request.user
    docs_path = os.path.join(settings.DOCS_DIR, path)
    if os.path.isdir(docs_path):
        path = os.path.join(path, "index.html")
    path = os.path.join(settings.DOCS_STATIC_NAMESPACE, path)
    return serve(request, path)
