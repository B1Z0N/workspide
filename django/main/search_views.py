from django.shortcuts import render
from django.http import Http404
import json


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