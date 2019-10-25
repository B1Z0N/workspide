from django.shortcuts import render
from django.http import Http404
import json

from .forms import AdModelForm


def search(request, _type, _text):
    if _type != 'jobs' and _type != 'workers':
        raise Http404()

    return render(
        request, 
        'search.html',
        # json.dumps(
            {'search_type' : _type, 
            'search_text' : _text}
        # ),
    )


def empty_search(request, _type): 
    return search(request, _type, "")


def add_ad(request):
    if request.method == 'POST':
        form = AdModelForm(instance=request.user, data=request.POST)
        if form.is_valid():
            pass
    else:
        form = AdModelForm()

    return render(request, 'ads/add_ad.html', { 'form' : form })
