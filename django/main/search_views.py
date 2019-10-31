from django.shortcuts import render, redirect
from django.http import Http404
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from datetime import datetime
from django.utils import timezone
import random
import json

from .forms import AdModelForm, PideModelForm
from .models import User, Ad, Skill, PetProject, Responsibility, Pide
from .email import send_mail

##################################################
# Search views
##################################################


def search(request, _type, _text):
    if _type != 'jobs' and _type != 'employees':
        raise Http404()

    return render(request, 'search.html', {
        'search_type': _type,
        'search_text': _text,
    })


def empty_search(request, _type):
    return search(request, _type, "")


##################################################
# Helper functions
##################################################

def negate_ad(ad_type):
    assert(ad_type == "vacancy" or ad_type == "resume")
    return 'vacancy' if ad_type == 'resume' else 'resume'


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


def ad_alert(request, msg=None):
    return render(request, 'alerts/render_base.html', {
        'response_error_title': 'Message',
        'response_error_text': 'No such ad exist'
        if msg is None else msg
    })


##################################################
# Ad creation/show/edit/delete/ views
##################################################


def add_ad(ad_type):
    assert(ad_type == "vacancy" or ad_type == "resume")

    def actual_view(request):
        form = AdModelForm(
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
    def assign(context, var, name):
        if var:
            context[name] = var

    def emptify(s): return '' if s is None else s

    def actual_view(request, ad, template_name):
        context = {'ad': ad, 'negated_type': negate_ad(ad.ad_type), }
        assign(context, Skill.objects.filter(ad_id=ad_id), 'skills')
        assign(context, ad.text, 'description')
        user = ad.uid

        if user.first_name or user.last_name:
            assign(context, emptify(user.first_name) +
                   ' ' + emptify(user.last_name), 'name')

        if ad.ad_type == 'vacancy':
            assign(context, Responsibility.objects.filter(
                vacancy_id=ad_id), 'resps')
        elif ad.ad_type == 'resume':
            assign(context, PetProject.objects.filter(
                resume_id=ad_id), 'projects')

        return render(request, template_name, context)

    def show_anonymous_ad(request, ad): return actual_view(
        request, ad, 'ads/ad_view.html')
    def show_foreign_ad(request, ad): return actual_view(
        request, ad, 'ads/ad_foreign_view.html')

    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        return ad_alert(request)
    if request.user == ad.uid or not request.user.is_authenticated:
        return show_anonymous_ad(request, ad)
    else:
        return show_foreign_ad(request, ad)


def edit_ad(ad_type):
    assert(ad_type == 'resume' or ad_type == 'vacancy')

    def actual_view(request, ad_id):
        try:
            ad = Ad.objects.get(id=ad_id)
        except Ad.DoesNotExist:
            return ad_alert(request)
        if ad_type != ad.ad_type:
            return ad_alert(request)
        if request.user != ad.uid:
            return ad_alert(request, msg='Na ah, you are not allowed to do this!')

        form = AdModelForm(
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
        return ad_alert(request)

    if request.user != ad.uid:
        return ad_alert(request, msg='Na ah, you are not allowed to do this!')

    if request.method == 'POST':
        ad.delete()
        return redirect('/account/')

    return render(request, 'ads/delete_ad.html', {'ad': ad})


def pide(request, ad_id):
    def actual_view(request, ad):
        form = PideModelForm(
            user=request.user, ad_type=negate_ad(ad.ad_type)
        )

        if request.method == 'POST':
            form = PideModelForm(data=request.POST,
                                 user=request.user, ad_type=negate_ad(
                                     ad.ad_type))
            if form.is_valid():
                pide = form.save(commit=False)
                pide.ad_to = ad
                pide.uid_from = request.user
                pide.uid_from.not_read += 1
                pide.ad_to.uid.not_read += 1
                pide.uid_from.save()
                pide.ad_to.uid.save()
                pide.save() 
                return redirect('/feed/')

        return render(request, 'deals/deal_base.html', {'form': form})

    try:
        ad = Ad.objects.get(id=ad_id)
    except Ad.DoesNotExist:
        return ad_alert(request)
    if request.user == ad.uid:
        return ad_alert(request, 'You are not allowed to pide your own ad')
    else:
        return actual_view(request, ad)


def feed(request):
    pides = Pide.objects.filter(ad_to__uid=request.user) | Pide.objects.filter(uid_from=request.user)
    _pides =[]
    for pide in pides.order_by('-pub_dtime'):
        if request.user.not_read:
            _pides.append((pide, 'marked'))
            request.user.not_read -= 1
        else:
            _pides.append((pide, 'usual'))
    request.user.save()
    return render(request, 'deals/feed_base.html', {
        'pides' : _pides,
    })


def pide_confirm(request, pide_id):
    def actual_view(request, pide):
        if request.method == 'POST':
            if 'reject_btn' in request.POST:
                if pide.ad_to.uid.not_read:
                    pide.ad_to.uid.not_read -= 1
                pide.uid_from.not_read += 1
                pide.state = 'rejected'
                pide.pub_dtime = timezone.now()
            elif 'accept_btn' in request.POST:
                pide.uid_from.not_read += 1
                pide.state = 'accepted'
                current_site = get_current_site(request)
                get_link = lambda ad: f"<a href='http://{current_site}/show_ad/{ad.id}/'>'{ad.title}'</a>"

                msg = f"Here is an email of {get_link(pide.ad_to)} {pide.ad_to.ad_type} owner, that you've pided:" 
                if pide.ad_from:
                    msg += msg[:-1] + f" with {get_link(pide.ad_from)} at {pide.pub_dtime}:"
                msg += f"  {pide.ad_to.uid.email}"
                send_mail(
                    subject='Pide success',
                    message=msg,
                    to_email=[pide.uid_from.email]
                )

                msg = f"Here is an email of "
                if pide.ad_from:
                    msg += f"{get_link(pide.ad_from)} {pide.ad_from.ad_type} owner"
                else:
                    msg += "user"
                msg += f""" that have pided you on {get_link(pide.ad_to)} at {pide.pub_dtime}:  {pide.uid_from.email}"""
                send_mail(
                    subject='Pide success',
                    message=msg,
                    to_email=[pide.ad_to.uid.email]
                )
            pide.pub_dtime = timezone.now()
            pide.uid_from.save()
            pide.ad_to.uid.save()
            pide.save()
            return redirect('/feed/')
        return render(request, 'deals/pide_confirm.html/', {
            'pide' : pide,
        })

    try:
        pide = Pide.objects.get(id=pide_id)
    except Pide.DoesNotExist:
        return ad_alert(request, 'No such pide exists')
    if pide.state == 'rejected':
        return ad_alert(request, 'This pide was rejected to you')
    elif pide.state == 'accepted':
        return ad_alert(request, 'This pide was accepted, author`s contacts is in pide author`s mailbox now')
    elif request.user == pide.ad_to.uid:
        return actual_view(request, pide)

    return ad_alert(request, 'You have no rights to go here, take care')
