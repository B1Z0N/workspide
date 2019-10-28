from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
import random
import json

from .forms import AdModelForm
from .models import User, Ad, Skill, PetProject, Responsibility


##################################################
# Search views
##################################################


def search(request, _type, _text):
    if _type != 'jobs' and _type != 'employees':
        raise Http404()

    return render(request, 'search.html', {
        'search_type': _type,
        'search_text': _text
    })


def empty_search(request, _type):
    return search(request, _type, "")


##################################################
# Helper functions
##################################################


def save_skills(post, ad):
    i = 1
    last = post.get('skill1')
    while last is not None:
        Skill.objects.create(text=last, ad_id=ad).save()
        i += 1
        last = post.get('skill' + str(i))


def save_resp(post, ad):
    i = 1
    last = post.get('resp1')
    while last is not None:
        Responsibility.objects.create(text=last, vacancy_id=ad).save()
        i += 1
        last = post.get('resp' + str(i))


def save_projects(post, ad):
    i = 1
    last_text = post.get('project_text1')
    last_link = post.get('project_link1')
    while last_text is not None:
        PetProject.objects.create(
            text=last_text, link=last_link, resume_id=ad).save()
        i += 1
        last_text = post.get('project_text' + str(i))
        last_link = post.get('project_link' + str(i))


def save_all_additional(post, ad, ad_type):
    save_skills(post, ad)
    if ad_type == 'vacancy':
        save_resp(post, ad)
    elif ad_type == 'resume':
        save_projects(post, ad)



# just a summernote placeholder generator
def get_description_placeholder(ad_type):
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

    if ad_type == 'vacancy':
        return ' '.join([gen_radnom_vacancy_beginning(), gen_random_job()])
    else:
        return ' '.join([gen_random_resume_beginning(), gen_random_job()])

def ad_error(request, msg=None):
    return render(request, 'alerts/render_base.html', {
        'response_error_title': 'Error',
        'response_error_text': 'No such ad exist' 
                                    if msg is None else msg
    })


##################################################
# Ad creation/show/edit/delete/ views
##################################################


def add_ad(ad_type):
    assert(ad_type == "vacancy" or ad_type == "resume")

    def actual_view(request):
        form = AdModelForm.get_form(
            text_widget_attrs={
                'placeholder': get_description_placeholder(ad_type)}
        )
        if request.method == 'POST' and 'submit_button' in request.POST:
            data = request.POST.copy()
            data['ad_type'] = ad_type
            form = AdModelForm(data=data)
            if form.is_valid():
                ad = form.save(commit=False)
                ad.uid = request.user

                ad.save()
                save_all_additional(request.POST, ad, ad_type)

                return redirect('/account/')

        context = {
            'form': form,
            ad_type: 'True',
            'title': 'New ' + ad_type,
        }

        return render(request, 'ads/add_ad.html', context)

    return actual_view


def show_ad(request, ad_id):
    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        return ad_error(request)

    def assign(context, var, name):
        if var:
            context[name] = var

    context = {'ad': ad, }
    assign(context, Skill.objects.filter(ad_id=ad_id), 'skills')
    assign(context, ad.text, 'description')
    user = ad.uid
    def emptify(s): return '' if s is None else s
    if user.first_name or user.last_name:
        assign(context, emptify(user.first_name) +
               ' ' + emptify(user.last_name), 'name')

    if ad.ad_type == 'vacancy':
        assign(context, Responsibility.objects.filter(
            vacancy_id=ad_id), 'resps')
    elif ad.ad_type == 'resume':
        assign(context, PetProject.objects.filter(resume_id=ad_id), 'projects')

    return render(request, 'ads/ad_view.html', context)


def edit_ad(ad_type):
    assert(ad_type == 'resume' or ad_type == 'vacancy')

    def actual_view(request, ad_id):
        try:
            ad = Ad.objects.get(id=ad_id)
        except Ad.DoesNotExist:
            return error(request)
        if ad_type != ad.ad_type:
            return error(request)

        form = AdModelForm.get_form(
            text_widget_attrs={
                'placeholder': get_description_placeholder(ad.ad_type)},
            instance=ad
        )
        if request.method == 'POST' and 'submit_button' in request.POST:
            data = request.POST.copy()
            data['ad_type'] = ad_type
            form = AdModelForm(data=data)
            if form.is_valid():
                ad.delete()
                ad = form.save(commit=False)
                ad.uid = request.user
                ad.save()
                save_all_additional(request.POST, ad, ad_type)
                return redirect('/account/')
        context = {
            'form': form,
            ad_type: 'True',
            'title': 'Edit ' + ad_type,
            'skills': Skill.objects.filter(ad_id=ad),
        }
        if ad_type == 'vacancy':
            context['resps'] = Responsibility.objects.filter(vacancy_id=ad)
        elif ad_type == 'resume':
            context['projects'] = [
                (resp.text, resp.link) for resp in
                PetProject.objects.filter(resume_id=ad)
            ]

        return render(request, 'ads/edit_ad.html', context)

    return actual_view


def delete_ad(request, ad_id):
    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        return ad_error(request)

    if request.user != ad.uid:
        return ad_error(request, msg='Na ah, you are not allowed to do this!')

    if request.method == 'POST':
        ad.delete()
        return redirect('/account/')

    return render(request, 'ads/delete_ad.html', {'ad': ad})
