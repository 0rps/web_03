from django.http import HttpResponse, HttpResponseNotFound


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def return_404(request, *args, **kwargs):
    return HttpResponseNotFound()
    