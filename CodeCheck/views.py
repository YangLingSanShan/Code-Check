from django.contrib.auth.decorators import login_required
from django.shortcuts import render


# @login_required(login_url='/users/login/')
def home_page(request):
    if not request.user.is_authenticated:
        return render(request, 'index.html')
    return render(request, 'menu.html')


@login_required(login_url='/users/login/')
def code_check(request):
    return render(request, 'codesCompare.html')


@login_required(login_url='/users/login/')
def history(request):
    return render(request, 'history.html')


@login_required(login_url='/users/login/')
def group_check(request):
    return render(request, 'groupCompare.html')