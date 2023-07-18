from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect

from MainApp.models import Snippet
from forms import SnippetForm, UserRegistrationForm


def index_page(request):
    if request.method == "POST":
        snippet_id = request.POST.get('snippet_id')
        try:
            snippet = Snippet.objects.get(id=snippet_id)
            context = {
                'snippet': snippet,
                'type': 'view'
            }

            return render(request, 'pages/snippet_detail.html', context)

        except ObjectDoesNotExist:
            raise Http404(f'Snippet with id = {snippet_id} does not exist')

    if request.method == "GET":
        context = {'pagename': 'PythonBin'}
        return render(request, 'pages/index.html', context)


@login_required
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
            snippet = form.save(commit=False)
            if request.user.is_authenticated:
                snippet.user = request.user
                snippet.save()

            return redirect('snippets_list')

        else:
            return render(request, 'pages/add_snippet.html', {'form': form})


def snippets_page(request):
    snippets = Snippet.objects.filter(is_public=True)
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


def snippet_edit(request, snippet_id):
    try:
        snippet = Snippet.objects.get(id=snippet_id)

    except ObjectDoesNotExist:
        raise Http404

    if request.method == 'GET':
        context = {
            'pagename': 'Edit snippet',
            'snippet': snippet,
            'type': 'edit'
        }

        return render(request, 'pages/snippet_detail.html', context)

    if request.method == 'POST':
        form_data = request.POST
        snippet.name = form_data['name']
        snippet.code = form_data['code']
        snippet.creation_date = form_data['creation_date']
        snippet.is_public = form_data.get('is_public', False)
        snippet.save()

        return redirect('snippets_list')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
        else:
            context = {
                'pagename': 'PythonBin',
                'errors': ['Wrong username or password']
            }

            return render(request, 'pages/index.html', context)

        return redirect('home')


def logout(request):
    auth.logout(request)

    return redirect('home')


@login_required
def my_snippets(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'My snippets',
        'snippets': snippets
    }

    return render(request, 'pages/view_snippets.html', context)


def create_user(request):
    if request.method == 'GET':
        form = UserRegistrationForm()
        context = {
            'pagename': 'Registration of new user',
            'form': form
        }

        return render(request, 'pages/register.html', context)

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')

        else:
            return render(request, 'pages/register.html', {'form': form})
