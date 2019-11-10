
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site

from django.utils import timezone

from main.forms import PideModelForm
from main.models import User, Ad, Pide
from main.email import send_mail

from djmoney.money import Money

from html_sanitizer import Sanitizer
sanitizer = Sanitizer()
sanitizer.tags = set(sanitizer.tags).union(['p', 'span', 'i', 'u', 'hr', 'ol', 'li', 'br', 'blockquote', 'ul', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])


def pide(request, ad_id):
    def actual_view(request, ad):
        form = PideModelForm(
            user=request.user, ad_type=negate_ad(ad.ad_type),
        )

        if request.method == 'POST':
            form = PideModelForm(data=request.POST,
                                 user=request.user, ad_type=negate_ad(
                                     ad.ad_type))
            if form.is_valid():
                pide = form.save(commit=False)
                pide.ad_to = ad
                pide.uid_from = request.user
                pide.comment = sanitizer.sanitize(pide.comment)
                pide.uid_from.not_read += 1
                pide.ad_to.uid.not_read += 1
                pide.uid_from.save()
                pide.ad_to.uid.save()
                pide.save() 
                return redirect('/feed/')

        return render(request, 'deals/deal_base.html', {'form': form})

    try:
        ad = Ad.objects.get(id=ad_id)
        # SELECT * FROM Ad WHERE id = ad_id 
    except Ad.DoesNotExist:
        return ad_alert(request)
    if request.user == ad.uid:
        return ad_alert(request, 'You are not allowed to pide your own ad')
    else:
        return actual_view(request, ad)


def feed(request):
    pides = \
        Pide.objects.filter(ad_to__uid=request.user) |\
        Pide.objects.filter(uid_from=request.user)
        # SELET * FROM Pide WHERE uid_from_id = request.user.id

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
        # SELECT * FROM Pide WHERE id = pide_id
    except Pide.DoesNotExist:
        return ad_alert(request, 'No such pide exists')
    if pide.state == 'rejected':
        return ad_alert(request, 'This pide was rejected to you')
    elif pide.state == 'accepted':
        return ad_alert(request, 'This pide was accepted, author`s contacts is in pide author`s mailbox now')
    elif request.user == pide.ad_to.uid:
        return actual_view(request, pide)

    return ad_alert(request, 'You have no rights to go here, take care')
