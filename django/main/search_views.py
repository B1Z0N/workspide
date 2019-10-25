from django.shortcuts import render
from django.http import Http404
import json

from .forms import AdModelForm, SKillModelForm, PetProjectModelForm, ResponsibilityModelForm


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


def add_ad(ad_type):
    assert(ad_type == "vacancy" or ad_type == "resume")

    def gen_random_job():
        import random
        ABSOLUTELY_ONE_HUNDRED_PERCENT_NOT_WEIRD_JOBS = [
            'sleeper',
            'drying paint watcher',
            'full-time netflix viewer',
            'train pusher',
            'professional mourner',
            'snake milker',
            'dog food taster',
            'odour judge',
            'marmite taster',
            'scuba diving pizza delivery man',
        ]
        return random.choice(ABSOLUTELY_ONE_HUNDRED_PERCENT_NOT_WEIRD_JOBS)
    
    def actual_view(request):
        form = AdModelForm()

        if request.method == 'POST':
            if 'submit_btn' in request.POST:
                form = AdModelForm(instance=request.user, data=request.POST)
                if form.is_valid():
                    form.cleaned_data['ad_type'] = ad_type
        
        context = { 
            'vacancy' : 'True',
            'title' : 'New vacancy',
            'text_placeholder' : 'Looking for experienced ' + gen_random_job(),
        } if ad_type == "vacancy" else { 
            'resume' : 'True',
            'title' : 'New resume',
            'text_placeholder' : 'Hello there, i am professional ' + gen_random_job(),
        }
        context['form'] = form
        
        return render(request, 'ads/add_ad.html', context)

    return actual_view
