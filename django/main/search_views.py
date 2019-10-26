from django.shortcuts import render
from django.http import Http404
from django.conf import settings
import random

from .forms import AdModelForm, SKillModelForm, PetProjectModelForm, ResponsibilityModelForm


def search(request, _type, _text):
    if _type != 'jobs' and _type != 'employees':
        raise Http404()

    return render(request, 'search.html', {
            'search_type' : _type, 
            'search_text' : _text
    })


def empty_search(request, _type):
    return search(request, _type, "")


# just a summernote placeholder generator
def set_description_placeholder(ad_type):
    assert(ad_type == "vacancy" or ad_type == "resume")

    def gen_random_job():
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

    def gen_random_resume_beginning():
        RESUME_BEGINNING = [
            'Hallo there. I`m a professional',
            'Greetings. I`m a passionate',
            'Aloha. I`m a highly qualified',
            'Ni hao. Wo hen zhuanye',
            'Hi. I see myself as',
            'Sometimes I just go to the beach, look at the waves and feel thankfull that I am a',
        ]
        return random.choice(RESUME_BEGINNING)

    def gen_radnom_vacancy_beginning():
        VACANCY_BEGINNING = [
            'Serious company is looking for serious(not funny)',
            'We found ourselves looking for an employee like',
            'Looking for experienced',
            'Posting job for a position of ',
            'Can`t wait to see YOU at position of'
        ]
        return random.choice(VACANCY_BEGINNING)

    def set_summernote_placeholder(placeholder):
        settings.SUMMERNOTE_CONFIG['summernote']['placeholder'] = placeholder 
    
    if ad_type == 'vacancy':
        set_summernote_placeholder(
            ' '.join([gen_radnom_vacancy_beginning(), gen_random_job()])
        )
    else:
        set_summernote_placeholder(
            ' '.join([gen_random_resume_beginning(), gen_random_job()])
        )


def add_ad(ad_type):
    assert(ad_type == "vacancy" or ad_type == "resume")

    def actual_view(request):
        form = AdModelForm()

        if request.method == 'POST' and 'submit_button' in request.POST:
            pass

        context = {
            'form' : form,
            ad_type : 'True',
            'title' : 'New ' + ad_type,
        }
        set_description_placeholder(ad_type)
        
        return render(request, 'ads/add_ad.html', context)

    return actual_view
