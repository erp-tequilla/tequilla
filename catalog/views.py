import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
import importlib

from django.template.loader import render_to_string

from catalog.models import MainEmployees
from tequilla.decorators import group_required


CATALOG_DATA = {
    'clubtype': {
        'title': 'Типы заведения',
        'new_item_text': 'Добавить новый тип заведения',
        'class_name': 'ClubType',
        'module_name': 'club.models',
        'form_class_name': 'ClubTypeForm',
        'form_module_name': 'club.forms',
        'filters': [
            {'name': 'name__icontains', 'type': 'text', 'prop': 'name', 'label': 'Название'}
        ]
    },
    'metro': {
        'title': 'Станции метро',
        'new_item_text': 'Добавить новую станцию метро',
        'class_name': 'Metro',
        'module_name': 'club.models',
        'form_class_name': 'MetroForm',
        'form_module_name': 'club.forms',
        'filters': [
            {'name': 'id__exact', 'type': 'text', 'prop': 'id', 'label': 'ID'},
            {'name': 'name__icontains', 'type': 'text', 'prop': 'name', 'label': 'Название'},
        ]
    },
    'uniform': {
        'title': 'Форма',
        'new_item_text': 'Добавить новую форму',
        'class_name': 'Uniform',
        'module_name': 'uniform.models',
        'form_class_name': 'UniformEditForm',
        'form_module_name': 'uniform.forms',
        'filters': [
            {'name': 'id__exact', 'type': 'text', 'prop': 'id', 'label': 'ID'},
            {'name': 'name__icontains', 'type': 'text', 'prop': 'name', 'label': 'Название'},
            {'name': 'num__exact', 'type': 'text', 'prop': 'num', 'label': 'Позиция'},
        ]
    },
    'penaltytype': {
        'title': 'Типы штрафов',
        'new_item_text': 'Добавить новый тип штрафа',
        'class_name': 'PenaltyType',
        'module_name': 'extuser.models',
        'form_class_name': 'PenaltyTypeForm',
        'form_module_name': 'extuser.forms',
        'filters': [
            {'name': 'description__icontains', 'type': 'text', 'prop': 'description', 'label': 'Описание'},
            {'name': 'num__exact', 'type': 'text', 'prop': 'num', 'label': 'Номер'},
            {'name': 'sum__exact', 'type': 'text', 'prop': 'sum', 'label': 'Сумма'},
            {'name': 'dismissal', 'type': 'select', 'prop': 'dismissal', 'label': 'Возможно увольнение'},
        ]
    }
}


def class_for_name(module_name, class_name):
    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)
    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)
    return c


@login_required
@group_required('director', 'chief', 'coordinator')
def catalog_list(request, item_type):
    if item_type not in CATALOG_DATA:
        return Http404
    data = CATALOG_DATA[item_type]
    Class = class_for_name(data['module_name'], data['class_name'])
    items = Class.objects.all()

    return render(
        request,
        'catalog/list.html',
        {
            'data': data,
            'items': items,
            'item_type': item_type,
            'filter_link': reverse('catalog:catalog_filter', kwargs={'item_type': item_type})
        }
    )


@login_required
@group_required('director', 'chief', 'coordinator')
def main_employees(request):
    if request.method == 'POST':
        pass
    return render(
        request,
        'catalog/main_employees.html',
        {
            'item': MainEmployees.get_file()
        }
    )



@login_required
@group_required('director', 'chief', 'coordinator')
def catalog_filter(request, item_type):
    if item_type not in CATALOG_DATA:
        data = '%s(%s);' % (request.GET['callback'], json.dumps({'items': ''}))
        return HttpResponse(data, "text/javascript")
    data = CATALOG_DATA[item_type]
    Class = class_for_name(data['module_name'], data['class_name'])
    if 'callback' in request.GET:
        object_list = Class.objects
        filters = [f['name'] for f in data['filters']]
        was_filtered = False
        for filter_name in filters:
            filter_value = request.GET.get(filter_name, '')
            if filter_value:
                filter_pack = {filter_name: filter_value}
                object_list = object_list.filter(**filter_pack)
                was_filtered = True
        if not was_filtered:
            object_list = object_list.all()

        rendered_blocks = {
            'items': render_to_string(
                'catalog/_list.html',
                {'items': object_list, 'item_type': item_type, 'data': data}
            ),
        }
        data = '%s(%s);' % (request.GET['callback'], json.dumps(rendered_blocks))
        return HttpResponse(data, "text/javascript")


@login_required
@group_required('director', 'chief', 'coordinator')
def catalog_edit(request, item_type, item_id=None):
    if item_type not in CATALOG_DATA:
        return Http404
    data = CATALOG_DATA[item_type]
    Class = class_for_name(data['module_name'], data['class_name'])
    Form = class_for_name(data['form_module_name'], data['form_class_name'])
    try:
        item = Class.objects.get(id=item_id)
    except Class.DoesNotExist:
        item = Class()

    if request.method == 'POST':
        form = Form(instance=item, data=request.POST)
        if form.is_valid():
            item = form.save()
            messages.add_message(request, messages.INFO, 'Информация успешно сохранена')
            return redirect('catalog:catalog_edit', item_type=item_type, item_id=item.id)
    else:
        form = Form(instance=item)

    return render(
        request,
        'catalog/edit.html',
        {
            'data': data,
            'item': item,
            'item_type': item_type,
            'form': form
        }
    )


@login_required
@group_required('director', 'chief', 'coordinator')
def catalog_remove(request, item_type, item_id):
    pass