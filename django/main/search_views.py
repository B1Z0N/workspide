from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
import random
import json

from .forms import AdModelForm
from .models import User, Ad, Skill, PetProject, Responsibility


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
            PetProject.objects.create(text=last_text, link=last_link, resume_id=ad).save()
            i += 1
            last_text = post.get('project_text' + str(i))
            last_link = post.get('project_link' + str(i))

    def save_all_additional(post, ad, ad_type):
        save_skills(post, ad)
        if ad_type == 'vacancy':
            save_resp(post, ad)
        elif ad_type =='resume':
            save_projects(post, ad)

    def actual_view(request):
        form = AdModelForm()

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
            'form' : form,
            ad_type : 'True',
            'title' : 'New ' + ad_type,
        }
        set_description_placeholder(ad_type)
        
        return render(request, 'ads/add_ad.html', context)

    return actual_view


# def edit_ad(ad_type):
#     assert(ad_type == "vacancy" or ad_type == "resume")
#     def actual_view(request, ad_id):
#         instance = Ad.objects.get(id=ad_id)
#         if not instance:
#             return render(request, 'alerts/render_base.html', {
#                 'response_error_title' : 'No',
#                 'response_error_text' : ad_type[0].upper() + ad_type[1:]  + \
#                     ' you are trying to edit doesn`t exist'
#             })
    
#         context = {}
#         skills = Skill.objects.get(ad_id=instance)
#         if skills is not None:
#             context['skills'] = skills
#         if ad_type == 'vacancy':
#             resps = Responsibility.objects.get(vacancy_id=instance)
#             if resps is not None:
#                 context['resps'] = resps
#         elif ad_type == 'resume':
#             projects = PetProject.objects.get(resume_id=instance)
#             if projects is not None:
#                 context['projects'] = projects


        
def show_ad(request, ad_id):
    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        return render(request, 'alerts/render_base.html', {
            'response_error_title' : 'Error',
            'response_error_text' : 'No such ad exist'
        }) 

    def assign(context, var, name):
        if var:
            context[name] = var

    context = {'ad' : ad,}
    assign(context, Skill.objects.filter(ad_id=ad_id), 'skills')
    assign(context, ad.text, 'description')
    user = ad.uid
    emptify = lambda s: '' if s is None else s
    if user.first_name or user.last_name:
        assign(context, emptify(user.first_name) + ' ' + emptify(user.last_name), 'name')

    if ad.ad_type == 'vacancy':
        assign(context, Responsibility.objects.filter(vacancy_id=ad_id), 'resps')
    elif ad.ad_type == 'resume':
        assign(context, PetProject.objects.filter(resume_id=ad_id), 'projects')

    return render(request, 'ads/ad_view.html', context)