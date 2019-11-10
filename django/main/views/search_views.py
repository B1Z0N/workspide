from django.shortcuts import render, redirect
from djmoney.money import Money
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import operator

from main.forms import FiltersForm
from main.models import Ad


##################################################
# Search views
##################################################


def compare_money(money1, money2, operation):
    return operation(money1, Money(money2.amount, money1.currency))

def compare_experience(exp1, type1, exp2, type2, operation):
    to_months = lambda in_years: 12 * in_years
    return operation(
        to_months(exp1) if type1.startswith('year') else exp1,
        to_months(exp2) if type2.startswith('year') else exp2,
    )


def salary_filters(form, search_results):
    salary_to = form.cleaned_data['salary_to']
    salary_from = form.cleaned_data['salary_from']
    if salary_to is not None:
        salary_to = Money(salary_to, salary_from.currency)
    salary_search_results = []

    for ad in search_results:
        if ad.salary is not None:
            should_add = True
            if salary_from.amount != 0.0:
                should_add = should_add and compare_money(salary_from, ad.salary, operator.le)
            if salary_to is not None:
               should_add = should_add and compare_money(salary_to, ad.salary, operator.ge)

            if should_add:
                salary_search_results.append(ad)
        elif form.cleaned_data['without_salary'] is True:
            salary_search_results.append(ad)

    return form, salary_search_results


def experience_filters(form, search_results):
    experience_from = form.cleaned_data['experience_from']
    experience_to = form.cleaned_data['experience_to']
    experience_type = form.cleaned_data['experience_type']
    experience_search_results = []
    for ad in search_results:
        if ad.experience is not None:
            should_add = True
            if experience_from is not None:
                should_add = should_add and compare_experience(
                    experience_from, experience_type, 
                    ad.experience, ad.experience_type, operator.le
                )
            if experience_to is not None:
                should_add = should_add and compare_experience(
                    experience_to, experience_type, 
                    ad.experience, ad.experience_type, operator.ge
                )

            if should_add:
                experience_search_results.append(ad)
        elif form.cleaned_data['without_experience'] is True:
            experience_search_results.append(ad)

    return form, experience_search_results


def general_search_results(form, search_ad_type, search_text):
    order_by = form.cleaned_data['order_by']
    city = form.cleaned_data['city']
    if city:
        search_results = Ad.objects.filter(
            is_archived=False, 
            ad_type=search_ad_type,
            city=city,
            title__icontains=search_text,
        ).order_by(order_by)
        """ 
            SELECT * FROM Ad WHERE is_archived = False, ad_type = search_ad_type, 
                    city = city, title LIKE %search_text% ORDER BY order_by ASC
        """
        # `DESC` if order_by starts with `-` else `ASC`  
    else:
        search_results = Ad.objects.filter(
            is_archived=False, 
            ad_type=search_ad_type,
            title__icontains=search_text,
        ).order_by(order_by)
        """ 
            SELECT * FROM Ad WHERE is_archived = False, ad_type = search_ad_type, 
                    title LIKE %search_text% ORDER BY order_by ASC
        """
        # `DESC` if order_by starts with `-` else `ASC` 
    return form, search_results


def search(
    request, _type, _text='None', 
    _salary_from='None', _salary_to='None', _currency='USD', _without_salary='True',
    _experience_from='None', _experience_to='None', _experience_type='months', _without_experience='True',
    _city='None', _order_by='-pub_dtime'):
    assert(_type == 'jobs' or _type == 'employees')

    search_type = 'resume' if _type == 'employees' else 'vacancy'
    search_text = '' if _text == 'None' else _text
    search_results = []

    if request.method == 'POST':
        put_salary = None
        form = FiltersForm(data=request.POST)
        if form.is_valid():
            return redirect('/'.join(
                    [
                        '/search',
                        'type_' + str(_type), 
                        'text_' + (str(search_text) if search_text else 'None'),
                        '_'.join([
                            'salary', 
                            str(form.cleaned_data['salary_from'].amount), 
                            str(form.cleaned_data['salary_to']), 
                            str(form.cleaned_data['salary_from'].currency),
                        ]),
                        'without_salary_' + str(form.cleaned_data['without_salary']),
                        '_'.join([
                            'experience', 
                            str(form.cleaned_data['experience_from']), 
                            str(form.cleaned_data['experience_to']), 
                            str(form.cleaned_data['experience_type']),
                        ]),
                        'without_experience_' + str(form.cleaned_data['without_experience']),
                        'city_' + (str(form.cleaned_data['city']) if form.cleaned_data['city'] else 'None'),
                        'order_by_' + str(form.cleaned_data['order_by']),
                    ]
                ))
    else:
        put_salary = Money(_salary_from, _currency) if _salary_from != 'None' else Money(0.0, _currency)
        data = {
            'salary_from' : put_salary,
            'salary_to' : float(_salary_to) if _salary_to != 'None' else None,
            'without_salary' : True if _without_salary == 'True' else False,
            'experience_from' : int(_experience_from) if _experience_from != 'None' else None,
            'experience_to' : int(_experience_to) if _experience_to != 'None' else None,
            'experience_type' : _experience_type,
            'without_experience' : True if _without_experience == 'True' else False,
            'city' : '' if _city == 'None' else _city, 
            'order_by' : _order_by,
        }
        form = FiltersForm(data=data)
        if form.is_valid():
            form.cleaned_data['salary_from'] = put_salary
            form, search_results = salary_filters(
               *experience_filters(
                   *general_search_results(form, search_type, search_text)
               )
            )

            page  = request.GET.get('page', 1)
            search_results = Paginator(search_results, 10)
            try:
                ads = search_results.page(page)
            except PageNotAnInteger:
                ads = search_results.page(1)
            except EmptyPage:
                ads = search_results.page(search_results.num_pages)
            
            search_results = ads

    return render(request, 'search.html', {
        'form' : form,
        'search_type': _type,
        'search_text': search_text,
        
        'search_results' : search_results,

        'salary_from' : put_salary,
    })
