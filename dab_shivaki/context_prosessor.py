import random

from django.conf import settings
from django.shortcuts import render

def error_404(request, exception):
    return render(request, 'error_404.html')

def media(request):

    """

    Add media-related context variables to the context.

    """

    return {'MEDIA_URL': settings.MEDIA_URL}


