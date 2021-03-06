import base64
import json
import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

from extuser.forms import LoginForm, UserCreationForm, UserChangeForm, ChangePasswordForm, UserEditAdminForm, \
    ChangeAvatarForm
from extuser.models import ExtUser
from django.contrib.auth.models import Group

from django.db.models import Q

from penalty.models import Penalty
from private_message.utils import send_message_user_register, send_message_about_new_password
from reports.models import Report
from tequilla.decorators import group_required


@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserChangeForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Изменения сохранены.')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'profile/edit.html', {'form': form})


def auth_login(request):
    if request.user.is_authenticated():
        return redirect('wall_index')
    error = False
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(phone=phone, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('wall_index')
            else:
                error = True
        else:
            error = True
    else:
        login_form = LoginForm()

    return render(
        request,
        'profile/login.html',
        {'login_form': login_form, 'error': error, 'register_form': UserCreationForm()}
    )


@login_required
def auth_logout(request):
    logout(request)
    return redirect('profile:login')


def register(request):
    if request.user.is_authenticated():
        return redirect('wall_index')

    registered = False
    if request.method == 'POST':
        register_form = UserCreationForm(data=request.POST)
        if register_form.is_valid():
            register_form.save()
            user = ExtUser.objects.get(phone=register_form.cleaned_data['phone'])
            group = Group.objects.get(name='employee')
            user.groups.add(group)
            user.save()
            registered = True
            register_form = UserCreationForm()

            # отправка сообщения админу о регистрации нового юзера
            send_message_user_register(user)
    else:
        register_form = UserCreationForm()

    return render(
        request,
        'profile/login.html',
        {'register_form': register_form, 'login_form': LoginForm(), 'registered': registered}
    )


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            user.set_password(form.cleaned_data['new_password'])
            user.save()
            update_session_auth_hash(request, user)
            form = ChangePasswordForm()
            messages.add_message(request, messages.INFO, 'Пароль успешно изменен.')
    else:
        form = ChangePasswordForm()

    return render(
        request,
        'profile/change_password.html',
        {'form': form}
    )


@login_required
def change_avatar(request):
    if request.method == 'POST':
        form = ChangeAvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    return render(
        request,
        'profile/change_avatar.html',
        {}
    )


@login_required
def user_list(request):
    users = ExtUser.objects.filter(is_active=True)
    return render(
        request,
        'users/user_list.html',
        {'users': users, 'filter_user_link': 'http://' + request.get_host() + reverse('profile:user_filter')}
    )


@login_required
def user_filter(request):
    if 'callback' in request.GET:
        object_list = ExtUser.objects
        filters = ['surname__icontains', 'name__icontains', 'is_active']
        was_filtered = False
        for filter_name in filters:
            filter_value = request.GET.get(filter_name, '')
            if filter_value:
                filter_pack = {filter_name: filter_value}
                object_list = object_list.filter(**filter_pack)
                was_filtered = True
        avatar = request.GET.get('avatar', '')
        if avatar != '':
            if avatar == '0':
                object_list = object_list.filter(Q(avatar__isnull=True) | Q(avatar=''))
            else:
                object_list = object_list.filter(avatar__isnull=False).exclude(avatar__exact='')
            was_filtered = True
        if not was_filtered:
            object_list = object_list.all()

        rendered_blocks = {
            'users': render_to_string(
                'users/_user_list.html',
                {'users': object_list, 'edit_users_perm': request.user.has_perm('extuser.can_edit_users')}
            ),
        }
        data = '%s(%s);' % (request.GET['callback'], json.dumps(rendered_blocks))
        return HttpResponse(data, "text/javascript")


@login_required
def user_detail(request, user_id):
    user = get_object_or_404(ExtUser, id=user_id)
    penalties = Penalty.objects.filter(employee=user)
    return render(
        request,
        'users/user_detail.html',
        {
            'user_info': user,
            'shots_sum': sum([report.get_shots_sum() for report in Report.objects.filter(work_shift__employee=user)]),
            'penalty_sum': sum([penalty.get_sum() for penalty in penalties]),
            'penalty_count': penalties.count()
        }
    )


# просмотр активности сотрудника руководством
@login_required
@group_required('director', 'chief', 'coordinator')
def user_activity(request, user_id):
    user = get_object_or_404(ExtUser, id=user_id)
    return render(
        request,
        'users/user_auth_log.html',
        {'user_info': user}
    )


@login_required
@group_required('director', 'chief', 'coordinator')
def user_edit(request, user_id):
    user = get_object_or_404(ExtUser, id=user_id)
    # директора может редактировать только он сам
    if user.groups.filter(name='director').exists() and user != request.user:
        raise Http404
    if request.method == 'POST':
        form = UserEditAdminForm(instance=user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, 'Информация о пользователе успешно обновлена')
    else:
        form = UserEditAdminForm(instance=user)
    return render(
        request,
        'users/user_edit.html',
        {'user_info': user, 'form': form}
    )


@login_required
@group_required('director', 'chief', 'coordinator')
def reset_password(request, user_id):
    user = get_object_or_404(ExtUser, id=user_id)
    if user.groups.filter(name='director').exists():
        return JsonResponse({'complete': 0})
    new_password = '12345'
    user.set_password(new_password)
    user.save()
    # отправка уведомления
    send_message_about_new_password(request.user, user, new_password)
    return JsonResponse({'complete': 1})


@login_required
@group_required('director', 'chief', 'coordinator')
def user_delete(request, user_id):
    user = get_object_or_404(ExtUser, id=user_id)
    if not user.groups.filter(name='director').exists():
        user.is_active = False
        user.save()
    return redirect('user_list')


@login_required
@group_required('director', 'chief', 'coordinator')
def user_create(request):
    if request.method == 'POST':
        form = UserEditAdminForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_employee = form.save()
            new_employee.set_password('12345')
            new_employee.save()
            new_employee.groups.add(cd['group'])

            # клубы
            for club in cd['clubs']:
                new_employee.clubs.add(club)
            messages.add_message(request, messages.INFO, 'Новый сотрудник успешно добавлен')
            return redirect('user_edit', user_id=new_employee.id)
    else:
        form = UserEditAdminForm()
    return render(
        request,
        'users/user_edit.html',
        {'user_info': None, 'form': form}
    )


@csrf_exempt
@login_required
def upload_avatar(request):
    img = request.POST.get('croppedImage', '')
    imgdata = base64.b64decode(img.split(',')[-1])
    request.user.avatar_cropped = ContentFile(
        imgdata, str(random.randint(1, 100000)) + '_' + str(request.user.id) + '.png'
    )
    request.user.save()
    return JsonResponse({'complete': 1})
