from django.shortcuts import render


def handler404(request, exception):
    return render(request, 'alerts/render_base.html', {
        'response_error_title': 'Oops',
        'response_error_text': 'Seems like this page is illegal. I won`t tell anybody about this, now go <a href="/">your way</a>'
    })


def handler500(request):
    return render(request, 'alerts/render_base.html', {
        'response_error_title': 'Oops',
        'response_error_text': 'Something bad happened. Give it another try. Go <a href="/">your way</a>'
    })