from django.shortcuts import render, redirect
#from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import ConstructItemForm, ApplicationItemForm
from .models import ConstructItem, ApplicationItem
from django.urls import reverse
import json
from .env_variables import export_csv_path,export_all_construct_csv_path,export_all_application_csv_path
from django.db.models import Count
from django.conf import settings

import datetime
from django.utils import timezone


# utilities

def load_construct_number(json_file='app/meta.json'):
    with open(json_file,'r') as in_file:
        meta = json.load(in_file)
    # get the last construct number
    last_construct_number = meta['last_construct_number']
    return str(last_construct_number)



def generate_construct_number(json_file='app/meta.json'):
    # open  meta.json
    with open(json_file,'r') as in_file:
        meta = json.load(in_file)
    # get the last construct number
    last_construct_number = meta['last_construct_number']
    # increment the last construct number
    new_construct_number = last_construct_number + 1
    # update the meta.json
    meta['last_construct_number'] = new_construct_number
    with open(json_file, 'w') as outfile:
        json.dump(meta, outfile)
    # return the new construct number
    return str(new_construct_number)

# Create your views here.


def home(request):
    #username = request.user.username
    return render(request, 'app/home.html')


#def login_view(request):
#    # Login view logic goes here
#    return render(request,"app/login.html")


@staff_member_required
def entry(request):
    if request.method == 'POST':

        form = ConstructItemForm(request.POST)
        if form.is_valid():
            construct_item = form.save(commit=False)
            construct_item.save()
            generate_construct_number()  # update construct_number in meta.json
            return redirect(reverse('app:entry_success'))
    else:
        form = ConstructItemForm()

    construct_number = load_construct_number()  # Your construct number generation logic

    return render(request, 'app/entry.html', {'form': form, 'construct_number': construct_number})

@staff_member_required
def entry_success(request):
    return render(request, 'app/entry_success.html')

@staff_member_required
def search(request):
    if request.method == 'POST':
        construct_number = request.POST['construct_number']
        try:
            construct_item = ConstructItem.objects.get(construct_number=construct_number)
            application_items = ApplicationItem.objects.filter(construct_number=construct_number).order_by('-application_time')
            return render(request, 'app/search.html',
                          {'construct_item': construct_item, 'application_items': application_items})
        except ConstructItem.DoesNotExist:
            return render(request, 'app/search.html', {'construct_item': False})

        except ApplicationItem.DoesNotExist:
            return render(request, 'app/search.html', {'construct_item': construct_number, 'application_items': False})
    else:
        return render(request, 'app/search.html')

@staff_member_required
def apply_success(request):
    return render(request, 'app/apply_success.html')

@staff_member_required
def apply(request, construct_number):
    #construct_item = ConstructItem.objects.get(construct_number=construct_number)

    if request.method == 'POST':
        print('bbbbb')
        form = ApplicationItemForm(request.POST)

        #print(form)

        if form.is_valid():
            print('cccc')
            application_item = form.save(commit=False)
            #application_item.application_time = timezone.now()
            application_item.save()
            return redirect(reverse('app:apply_success'))

    try:
        application_items = ApplicationItem.objects.filter(construct_number=construct_number).order_by('-application_time')
    except ApplicationItem.DoesNotExist:
        return render(request, 'app/application.html', {'construct_number': construct_number})

    return render(request, 'app/application.html',
                  {'construct_number': construct_number, 'application_items': application_items})



@staff_member_required
def edit(request, construct_number):
    construct_item = ConstructItem.objects.get(construct_number=construct_number)
    if request.method == 'POST':
        form = ConstructItemForm(request.POST, instance=construct_item)
        if form.is_valid():
            form.save()
            return redirect('app:search')
    else:
        form = ConstructItemForm(instance=construct_item)

    return render(request, 'app/edit.html', {'form': form, 'construct_item': construct_item})


@staff_member_required
def delete(request, construct_number):
    construct_item = ConstructItem.objects.get(construct_number=construct_number)
    if request.method == 'POST':
        try:
            application_items = ApplicationItem.objects.filter(construct_number=construct_number).order_by(
                '-application_time')
            for application_item in application_items:
                application_item.delete()
        except ApplicationItem.DoesNotExist:
            pass
        construct_item.delete()
        return redirect('app:search')

    return render(request, 'app/delete.html', {'construct_item': construct_item})



def application(request):
    application_items = ApplicationItem.objects.filter(construct_item__user=request.user)
    return render(request, 'app/application.html', {'application_items': application_items})


def items_to_csv(a_items, csv_path, fields):
    import pandas as pd
    if a_items.exists():
        item_dicts = [{field: getattr(item, field) for field in fields} for item in a_items]
        df = pd.DataFrame(item_dicts)
        df.to_csv(csv_path, index=False)
        print(f"Exported to {csv_path}")
        return True
    else:
        return False  # no application_item filtered

@staff_member_required
def export(request):
    if request.method == 'POST':
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        start_year,start_month, start_day = tuple(start_date.split('-'))
        end_year, end_month, end_day = tuple(end_date.split('-'))
        #print(start_date)
        #print(type(start_date))
        start_date = timezone.datetime(int(start_year),int(start_month), int(start_day))
        end_date = timezone.datetime(int(end_year), int(end_month), int(end_day)+1)
        # Export logic goes here
        application_items = ApplicationItem.objects.filter(application_time__range=(start_date, end_date))
        application_field_names = [field.name for field in ApplicationItem._meta.get_fields() if field.name != "id"]

        import os
        file_full_path = os.path.join('app/static', export_csv_path)

        if items_to_csv(application_items,file_full_path,application_field_names):
            # Generate CSV file and return its URL
            return render(request, 'app/export.html', {'exported': True, 'csv_file_url': export_csv_path,'basename':os.path.basename(file_full_path)})
        else:
            return render(request, 'app/export.html',{'no_filtered_files': True})

    return render(request, 'app/export.html')
@staff_member_required
def statistics(request):

    constructItems = ConstructItem.objects.all().order_by('-application_time')
    applicationItems = ApplicationItem.objects.all().order_by('-application_time')

    len_constructItems = len(constructItems)
    len_applicationItems = len(applicationItems)
    len_receptors = ConstructItem.objects.values('receptor').annotate(user_count=Count('receptor')).count()
    user_count = ApplicationItem.objects.values('application_user').annotate(user_count=Count('application_user')).count()
    context = {
        'len_constructItems': len_constructItems,
        'len_applicationItems': len_applicationItems,
        'len_receptors': len_receptors,
        'user_count': user_count
               }

    construct_Items = ConstructItem.objects.all()
    application_items = ApplicationItem.objects.all()

    import os
    all_construct_full_path = os.path.join('app/static', export_all_construct_csv_path)
    all_application_full_path = os.path.join('app/static', export_all_application_csv_path)

    construct_field_names = [field.name for field in ConstructItem._meta.get_fields() if field.name != "id"]
    application_field_names = [field.name for field in ApplicationItem._meta.get_fields() if field.name != "id"]

    IF_CONSTRUCT_CREATED = items_to_csv(construct_Items, all_construct_full_path, construct_field_names)
    IF_APPLICATION_CREATED = items_to_csv(application_items, all_application_full_path, application_field_names)

    if IF_CONSTRUCT_CREATED:
        context['export_all_construct'] = True
        context['all_construct_csv_file_url'] = export_all_construct_csv_path
        context['all_construct_basename'] = os.path.basename(export_all_construct_csv_path)

    if IF_APPLICATION_CREATED:
        context['export_all_application'] = True
        context['all_application_csv_file_url'] = export_all_application_csv_path
        context['all_application_basename'] = os.path.basename(export_all_application_csv_path)

    return render(request, 'app/statistics.html', context)

