from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseNotFound
from django.shortcuts import render, redirect

from MainApp.models import Snippet
from forms import SnippetForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    if request.method == 'GET':
        form = SnippetForm()
        context = {
            'pagename': 'Добавление нового сниппета',
            'form': form
        }

        return render(request, 'pages/add_snippet.html', context)

    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pages/snippets_list')

        else:
            return render(request, 'pages/snippets_list', {'form': form})


def snippets_page(request):
    snippets = Snippet.objects.all()
    snippets_cnt = Snippet.objects.count()

    context = {
        'snippets': snippets,
        'snippets_cnt': snippets_cnt
    }

    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except ObjectDoesNotExist:
        return HttpResponseNotFound(f"<text>Snippet with id = {snippet_id} not found</text>")
    else:
        context = {
            'snippet': snippet
        }

        return render(request, 'pages/snippet_detail.html', context)


def snippet_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        lang = request.POST['lang']
        code = request.POST['code']
        snippet = Snippet(name=name, lang=lang, code=code)
        snippet.save()

        return redirect('snippets_list')
