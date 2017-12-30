from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_protect
from qa.models import Question, Answer
from qa.forms import AskForm, AnswerForm
from django.shortcuts import render
from django.template import RequestContext


def test(request, *args, **kwargs):
    return HttpResponse('OK')


def return_404(request, *args, **kwargs):
    return HttpResponseNotFound()


def recent(request):
    page = request.GET.get('page') or 1

    try:
        page = int(page)
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
    page = request.GET.get('page') or 1

    try:
        page = int(page)
    except ValueError:
        raise Http404

    limit = 10
    paginator = Paginator(Question.objects.popular(), limit)
    paginator.baseurl = 'popular/?page='

    try:
        page = paginator.page(page)
    except EmptyPage:
        page = paginator.page(max(paginator.num_pages-1, 0))

    return render(request,
                  'questions_list_template.html',
                  {'p': page,
                   'paginator': paginator})


@csrf_protect
def question(request, slug):
    try:
        pk = int(slug)
    except ValueError:
        raise Http404

    try:
        q = Question.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/question/%s/' % pk)
    else:
        form = AnswerForm(initial={'question': pk})

    answers = Answer.objects.filter(question=q).all()
    return render(request,
                  'question_template.html',
                  {'q': q,
                   'form': form,
                   'answers': answers})


@csrf_protect
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            q = form.save()
            return HttpResponseRedirect('/question/%s/' % q.pk)
    else:
        form = AskForm()
    return render(request, 'ask_template.html', {'form': form})
