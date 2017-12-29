from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseBadRequest
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from qa.models import Question, Answer
from django.shortcuts import render
from django.template import RequestContext


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def return_404(request, *args, **kwargs):
    return HttpResponseNotFound()


def recent(request):
    if 'page' not in request.GET:
        return HttpResponseBadRequest()

    try:
        page = int(request.GET.get('page'))
    except ValueError:
        raise Http404

    limit = 10
    paginator = Paginator(Question.objects.order_by('-added_at'), limit)
    paginator.baseurl = '/?page='

    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request,
                  'questions_list_template.html',
                  {'p': page,
                   'paginator': paginator})


def popular(request):
    if 'page' not in request.GET:
        return HttpResponseBadRequest()

    try:
        page = int(request.GET.get('page'))
    except ValueError:
        raise Http404

    limit = 10
    paginator = Paginator(Question.objects.popular, limit)
    paginator.baseurl = 'popular/?page='

    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request,
                  'questions_list_template.html',
                  {'p': page,
                   'paginator': paginator})


def question(request, slug):
    try:
        pk = int(slug)
    except ValueError:
        raise Http404

    try:
        q = Question.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404

    answers = Answer.objects.filter(question=q).all()

    return render(request,
                  'question_template.html',
                  {'q': q,
                   'answers': answers})
