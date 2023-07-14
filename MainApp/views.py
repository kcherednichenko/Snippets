from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
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
            return redirect('snippets_list')

        else:
            return render(request, 'pages/add_snippet.html', {'form': form})


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
        context = {
            'snippet': snippet,
            'type': 'view'
        }

        return render(request, 'pages/snippet_detail.html', context)

    except ObjectDoesNotExist:
        raise Http404


def snippet_delete(request, snippet_id):
    snippet = Snippet.objects.get(id=snippet_id)
    snippet.delete()

    # redirect to the same page, where request came from
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
