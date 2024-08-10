from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.core.files.base import ContentFile
import json

from django.views.decorators.http import require_http_methods

from .models import UserProfile
from .avatar_generate import IDicon


@csrf_protect
def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        if email:
            # Register
            if User.objects.filter(username=username).exists():
                return JsonResponse({'status': 'failure', 'message': '该用户名已存在'})
            elif User.objects.filter(email=email).exists():
                return JsonResponse({'status': 'failure', 'message': '该邮箱已被注册'})
            user = User.objects.create_user(username=username, password=password, email=email)
            user_profile, _ = UserProfile.objects.get_or_create(user=user)
            login(request, user)
            return JsonResponse({
                'status': 'success',
                'message': '注册成功',
                'username': username,
                'avatar': user_profile.avatar.url
            })
        else:
            # Login
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'status': 'success',
                    'message': '登录成功',
                    'username': username,
                    'avatar': user.userprofile.avatar.url
                })
            else:
                return JsonResponse({'status': 'failure', 'message': '用户名或密码错误'})

    return render(request, 'users/login.html')


@login_required
@require_http_methods(["GET"])
def user_logout(request):
    logout(request)
    return JsonResponse({'status': 200, 'logout': True})


def check_login(request):
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get_or_create(user=request.user)
        return JsonResponse({
            'status': 'success',
            'login': True,
            'username': request.user.username,
            'avatar': user_profile[0].avatar.url
        })
    else:
        return JsonResponse({'status': 'success', 'login': False})


@login_required
def change_password(request):
    if request.method == 'POST':
        user: User = request.user
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        new_password_confirm = request.POST.get('new_password_confirm')

        if not old_password or not new_password or not new_password_confirm:
            return JsonResponse({'status': 'failure', 'message': '缺少必填项'})
        if user.check_password(old_password):
            if new_password != new_password_confirm:
                return JsonResponse({'status': 'failure', 'message': '两次密码不一致'})
            user.set_password(new_password)
            user.save()
            login(request, user)
            return JsonResponse({'status': 'success', 'message': '修改成功'})
        else:
            return JsonResponse({'status': 'failure', 'message': '旧密码错误'})


@login_required
def change_username(request):
    if request.method == 'POST':
        user: User = request.user
        new_username = request.POST.get('new_username')

        if not new_username:
            return JsonResponse({'status': 'failure', 'message': '请填写新的用户名'})

        if User.objects.filter(username=new_username).exists():
            return JsonResponse({'status': 'failure', 'message': '该用户名已存在'})

        user.username = new_username
        user.save()

        return JsonResponse({'status': 'success', 'message': '修改成功'})


@login_required
def change_email(request):
    if request.method == 'POST':
        user: User = request.user
        new_email = request.POST.get('new_email')

        if not new_email:
            return JsonResponse({'status': 'failure', 'message': '请填写新的邮箱'})

        if User.objects.filter(email=new_email).exists():
            return JsonResponse({'status': 'failure', 'message': '该邮箱已被注册'})

        user.email = new_email
        user.save()

        return JsonResponse({'status': 'success', 'message': '修改成功'})


@login_required
def change_avatar(request):
    if request.method == 'POST':
        user: User = request.user
        avatar = request.FILES.get('avatar')

        if not avatar:
            return JsonResponse({'status': 'failure', 'message': '头像不能为空'})

        user_profile = UserProfile.objects.get(user=user)

        user_profile.avatar.save(avatar.name, ContentFile(avatar.read()))
        user_profile.save()

        return JsonResponse({'status': 'success', 'message': '修改成功'})
    # else:
    #     user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    #     return render(request, 'users/profile_test.html', {'user_profile': user_profile, 'user': request.user})


def random_avatar():
    image = IDicon()
    # 看后续有什么需求，怎么保存和使用这个image
